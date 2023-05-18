from typing import Dict

from sqlalchemy.sql.expression import select
from sqlalchemy.engine.row import Row
from app.infrastructure.postgres.postgres_connection import PostgresConnection
from app.models.graphQL.band_information import BandInformation
from app.models.graphQL.band_member import BandMember

from app.models.models import Member, Instrument, Genre, Band


class BandService:

    def __init__(self, conn: PostgresConnection) -> None:
        self._conn = conn
        self._create_tables()

    def get_bands_information(self, item: Dict) -> BandInformation:
        """
        Get Bands information from DB for the selected band
        :return:
        """
        try:
            with self._conn.get_session() as session:

                query = select(Band, Member.first_name, Member.family_name, Instrument.name, Genre.name)\
                    .where(Band.band_name == item['band_name'])\
                    .where(Band.band_id == Member.band_id)\
                    .where(Instrument.instrument_id == Member.instrument_id)\
                    .where(Band.genre_id == Genre.genre_id)

                print(f'inside service: {query}')
                result = session.execute(query)

                band_information = None
                for item in result:
                    if not band_information:
                        band = item[0]
                        band_information = BandInformation(band.band_id, band.band_name, item[4], [])
                        print(f'band info: {type(band_information)}')

                    print(f'second band info: {type(band_information.band_members)}')
                    band_information.band_members.append(self.convert_members_for_gql(row=item))

                return band_information
        except Exception as e:
            print(f'Could not get band information: {e}')

    def _create_tables(self) -> None:
        """
        It will only create the tables if they don't exist
        """
        engine = self._conn.get_engine()

        Genre.__table__.create(bind=engine, checkfirst=True)
        Instrument.__table__.create(bind=engine, checkfirst=True)
        Band.__table__.create(bind=engine, checkfirst=True)
        Member.__table__.create(bind=engine, checkfirst=True)

        print(f'meta: {Genre.__tablename__}')

    def convert_members_for_gql(self, row: Row) -> BandMember:
        """
        Convert Band Members to list for graphql query
        """
        return BandMember(row[1], row[2], row[3])
