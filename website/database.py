#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    database.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Database(object):

    def __init__(self):

        self.session_maker = sessionmaker()
        self.session = scoped_session(self.session_maker)
        self.engine = None



    def init(self, url, echo):

        self.engine = create_engine(url, echo=echo)
        self.session_maker.configure(bind=self.engine)



    def close_session(self):

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            db.session.remove()

class ScopedQuery(object):

    def __enter__(self):

        return self

    def __exit__(self, type, value, traceback):
        db.close_session()


db = Database()
db = SQLAlchemy(settings.SQLALCHEMY_DATABASE_URI, settings.SQLALCHEMY_DATABASE_ECHO)