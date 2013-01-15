#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    database.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import  settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()