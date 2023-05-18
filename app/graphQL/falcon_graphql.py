import json
from collections import OrderedDict
from types import SimpleNamespace

import falcon
from ariadne import graphql
from graphql import GraphQLSchema

# Adapted from https://github.com/alecrasmussen/falcon-graphql-server


class GraphQLResource:
    _ERROR_MESSAGE_QUERY = 'Must provide query string.'
    _ERROR_MESSAGE_JSON = 'Variables are invalid JSON.'

    def __init__(self, schema: GraphQLSchema):
        self.schema = schema

    def _get_context_value(self, req):
        return SimpleNamespace(
            request=req,
            loaders={}
        )

    async def _execute(self, params, req, resp):
        success, result = await graphql(
            self.schema,
            params,
            context_value=self._get_context_value(req)
        )

        status_code = falcon.HTTP_200 if success else falcon.HTTP_400
        resp.content_type = falcon.MEDIA_JSON
        resp.status = status_code
        resp.media = result

    def _send_error(self, resp, message):
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_400
        resp.media = {
            "errors": [{
                "message": message
            }]
        }

    async def on_get(self, req, resp):
        if req.params and 'query' in req.params and req.params['query']:
            query = str(req.params['query'])
        else:
            # this means that there aren't any query params in the url
            return self._send_error(resp, self._ERROR_MESSAGE_QUERY)

        variables = {}
        if 'variables' in req.params and req.params['variables']:
            try:
                variables = json.loads(str(req.params['variables']),
                                       object_pairs_hook=OrderedDict)
            except json.decoder.JSONDecodeError:
                return self._send_error(resp, self._ERROR_MESSAGE_JSON)

        operation_name = None
        if 'operationName' in req.params and req.params['operationName']:
            operation_name = str(req.params['operationName'])

        return await self._execute(
            {
                'query': query,
                'variables': variables,
                'operationName': operation_name,
            }, req, resp)

    async def _get_post_json_content(self, req, resp, query, variables, operation_name):

        try:
            post_data = await req.media
        except falcon.HTTPError:
            return self._send_error(resp, 'POST body sent invalid JSON.')

        # build the query string (Graph Query Language string)
        if query is None and post_data and 'query' in post_data:
            query = str(post_data['query'])
        elif query is None:
            return self._send_error(resp, self._ERROR_MESSAGE_QUERY)

        # build the variables string (JSON string of key/value pairs)
        if variables is None and post_data and 'variables' in post_data and post_data['variables']:
            variables = post_data['variables']
            if not isinstance(variables, dict):
                return self._send_error(resp, self._ERROR_MESSAGE_JSON)

        elif variables is None:
            variables = {}

        # build the operationName string (matches a query or mutation name)
        if operation_name is None and 'operationName' in post_data and post_data['operationName']:
            operation_name = str(post_data['operationName'])

        return query, variables, operation_name

    async def _get_post_graphql_content(self, req, resp, query):

        try:
            req.context['post_data'] = (await req.stream.read()).decode('utf-8')
            post_data = str(req.context['post_data'])
        except falcon.HTTPError:
            return self._send_error(resp, 'POST body sent invalid JSON.')

        # build the query string
        if query is None and post_data:
            query = post_data

        elif query is None:
            return self._send_error(resp, self._ERROR_MESSAGE_QUERY)

        return query

    async def on_post(self, req, resp):
        # parse url parameters in the request first
        query = req.get_param('query')

        variables = None
        if req.get_param('variables'):
            try:
                variables = json.loads(str(req.params['variables']), object_pairs_hook=OrderedDict)
            except json.decoder.JSONDecodeError:
                return self._send_error(resp, self._ERROR_MESSAGE_JSON)

        operation_name = req.get_param('operationName')
        # Handle 'content-type: application/json' requests
        if req.content_type and 'application/json' in req.content_type:
            post_json_content = await self._get_post_json_content(req, resp, query, variables, operation_name)

            if post_json_content is None:
                return
            (query, variables, operation_name) = post_json_content

        # Handle 'content-type: application/graphql' requests
        elif req.content_type and 'application/graphql' in req.content_type:
            query = await self._get_post_graphql_content(req, resp, query)
            if query is None:
                return

        elif query is None:
            # this means that the content-type is wrong and there aren't any
            # query params in the url
            return self._send_error(resp, self._ERROR_MESSAGE_QUERY)

        return await self._execute(
            {
                'query': query,
                'variables': variables,
                'operationName': operation_name,
            }, req, resp)

