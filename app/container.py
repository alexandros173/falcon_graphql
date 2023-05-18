from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.infrastructure.postgres.postgres_connection import PostgresConnection
from app.services.service_container import ServiceContainer
from config.general import Config


class AppContainer(DeclarativeContainer):

    config = providers.Dependency(instance_of=Config)

    postgres = providers.Singleton(PostgresConnection, config=config)

    services = providers.Container(ServiceContainer, database=postgres)


def build_app_container(config: Config) -> AppContainer:
    from app.graphQL import resolver

    try:
        container = AppContainer(config=config)
        container.wire(packages=[resolver])

        return container
    except Exception as e:
        print(f'Unable to create AppContainer: {e}')
