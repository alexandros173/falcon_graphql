
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = 'genre'

    genre_id = Column(Integer,
                      primary_key=True)
    name = Column(String(150))


class Instrument(Base):
    __tablename__ = 'instrument'

    instrument_id = Column(Integer,
                           primary_key=True)
    name = Column(String(150))


class Band(Base):
    __tablename__ = 'band'

    band_id = Column(Integer,
                     primary_key=True)
    band_name = Column(String(100))
    genre_id = Column(Integer, ForeignKey(Genre.genre_id))


class Member(Base):
    __tablename__ = 'member'

    member_id = Column(Integer,
                       primary_key=True)
    first_name = Column(String(70))
    family_name = Column(String(70))
    band_id = Column(Integer, ForeignKey(Band.band_id))
    instrument_id = Column(Integer, ForeignKey(Instrument.instrument_id))