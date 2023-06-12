import atexit
import os
from urllib.error import HTTPError
from graphql import GraphQLSchema

from ariadne import load_schema_from_path, snake_case_fallback_resolvers
from ariadne.contrib.federation import make_federated_schema
from app.api import start_server
from app.container import build_app_container
from app.graphQL.resolver import resolvers
from app.infrastructure.postgres.postgres_connection import PostgresConnection
from config.general import Config


class Server:
    def __init__(self):
        self.api = ''

    def get_default_schema(self):
        graphql_schema_path = os.path.join(os.path.dirname(__file__),
                                           'graphQL/schema')
        type_defs = load_schema_from_path(
            graphql_schema_path)  # Construct schema from all *.graphql

        return make_federated_schema(type_defs, resolvers, snake_case_fallback_resolvers)

    def start(self, schema: GraphQLSchema = None):
        graphql_schema = schema
        try:
            if graphql_schema is None:
                graphql_schema = self.get_default_schema()
            self.api = start_server(graphql_schema)

            return self.api

        except(OSError, HTTPError) as e:
            print(f'Unable to start Falcon server: {e}')


def on_exit_app():
    PostgresConnection.close()


config = Config()
container = build_app_container(config)

server = Server()
api = server.start()

atexit.register(on_exit_app)
