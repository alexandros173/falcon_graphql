from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers

from app.infrastructure.postgres.postgres_connection import PostgresConnection
from app.services.band_service import BandService


class ServiceContainer(DeclarativeContainer):

    database = providers.Dependency(instance_of=PostgresConnection)

    band_service = providers.Factory(BandService, conn=database)
