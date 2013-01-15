#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    models.py, in Briseis.
#
#
#    Created at 2013/01/15. Ruoyan Wong(@saipanno).

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = 'user_groups'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String(128), nullable=False)