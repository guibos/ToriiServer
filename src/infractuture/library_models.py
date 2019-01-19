"""Library models."""

from sqlalchemy import Column, Integer, Date, JSON, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

from src.infractuture.user_models import UserModel

BASE = declarative_base()


class Country(BASE):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    iso3166 = Column('iso3166', String(2))
    name = Column(JSON)


class Producer(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'producer'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


class Licensor(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'licensor'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


class Studio(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'studio'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


class Serialization(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'serialization'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


class Type(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


class Subtype(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'subtype'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)
    type = Column(ForeignKey(Type.id))
    mode = Column(Integer)


class Genre(BASE):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


class Status(BASE):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)


class Group(BASE):  # pylint: disable=too-few-public-methods
    """Group models. They are groups of units. One group can be member of another group."""
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    insert_date = Column(Date, nullable=False)
    name = Column(JSON)
    release_date = Column(Date)
    user_id = Column(ForeignKey(UserModel.id), nullable=False)


class Title(BASE):  # pylint: disable=too-few-public-methods
    """Unit model. They are are where are stored only one unit of the library."""
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True, autoincrement=True)
    insert_date = Column(Date, nullable=False)
    user_id = Column(ForeignKey(UserModel.id), nullable=False)
    data = Column(JSON)
    name = Column(JSON)
    subtype = Column(ForeignKey(Subtype.id))
    release_date = Column(Date)
    premiered = Column(JSON)
    score = Column(Integer)
    rating = Column(Integer)
    countries = relationship(Country, secondary='title_country', backref=__tablename__)
    groups = relationship(Group, secondary='group_title', backref=__tablename__)
    producers = relationship(Producer, secondary='title_producer', backref=__tablename__)
    licensors = relationship(Licensor, secondary='title_licensor', backref=__tablename__)
    studios = relationship(Studio, secondary='title_studio', backref=__tablename__)
    genres = relationship(Genre, secondary='title_genre', backref=__tablename__)


class TitleCountry(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'title_country'
    country = Column('country_id', ForeignKey(Country.id), primary_key=True)
    title = Column('title_id', ForeignKey(Title.id), primary_key=True)


class GroupTitle(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'group_title'
    group = Column('group_id', ForeignKey(Group.id), primary_key=True)
    title = Column('title_id', ForeignKey(Title.id), primary_key=True)


class TitleProducer(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'title_producer'
    title = Column('title_id', ForeignKey(Title.id), primary_key=True)
    producer = Column('producer_id', ForeignKey(Producer.id), primary_key=True)


class TitleLicensor(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'title_licensor'
    title = Column('title_id', ForeignKey(Title.id), primary_key=True)
    licensor = Column('licensor_id', ForeignKey(Licensor.id), primary_key=True)


class TitleStudio(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'title_studio'
    title = Column('title_id', ForeignKey(Title.id), primary_key=True)
    studio = Column('studio_id', ForeignKey(Studio.id), primary_key=True)


class TitleGenre(BASE):  # pylint: disable=too-few-public-methods
    __tablename__ = 'title_genre'
    title = Column('title_id', ForeignKey(Title.id), primary_key=True)
    genre = Column('genre_id', ForeignKey(Genre.id), primary_key=True)
