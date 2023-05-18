import falcon as falcon
import falcon.asgi
from graphql import GraphQLSchema

from app.access_middleware import AccessMiddleware
from app.graphQL.falcon_graphql import GraphQLResource
from config.general import Config


class Healthcheck:
    async def on_get(self, req, resp):
        resp.media = {"status": "healthy"}
        resp.status = falcon.HTTP_200


def start_server(schema: GraphQLSchema):
    api = falcon.asgi.App(middleware=[AccessMiddleware()])
    api.req_options.keep_blank_qs_values = True

    api.add_route('/healthcheck', Healthcheck())

    # GraphQL server
    graphql_server = GraphQLResource(schema)

    api.add_route('/', graphql_server)
    # api.add_route('/graphql', GraphQLPlaygound())

    return api
