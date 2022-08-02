from email.policy import default
import os

import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    search_results = relationship('SearchResult', back_populates='user')


class SearchParams(Base):
    __tablename__ = 'search_params'

    id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), primary_key=True)
    country_id = sq.Column(sq.Integer, nullable=True)
    city_id = sq.Column(sq.Integer, nullable=True)
    sex = sq.Column(sq.Integer, default=0)
    age_from = sq.Column(sq.Integer, default=0)
    age_to = sq.Column(sq.Integer, default=60)


class SearchResult(Base):
    __tablename__ = 'matches'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.String, nullable=False)
    last_name = sq.Column(sq.String, nullable=False)
    profile_link = sq.Column(sq.String, nullable=False)
    is_favorite = sq.Column(sq.Boolean, default=False)
    blacklisted = sq.Column(sq.Boolean, default=False)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
    user = relationship('User', back_populates='search_results')
    photos = relationship('Photo', back_populates='owner')
    
    


class Photo(Base):
    __tablename__ = 'Photos'

    id = sq.Column(sq.Integer, primary_key=True)
    url = sq.Column(sq.String, nullable=False)
    owner_id = sq.Column(sq.Integer, sq.ForeignKey('matches.id'))
    owner = relationship('SearchResult', back_populates='photos')
