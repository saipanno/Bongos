#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

import tornado.web
import tornado.locale

from web import settings as config

from web.helper import import_setting_from_config
from web.form import create_forms
from web.extensions.routing import route

from sqlalchemy import  create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from web.handler import ErrorHandler

class Application(tornado.web.Application):

    def __init__(self):
        settings = import_setting_from_config(config)

        handlers = route.get_routes()
        # Custom 404 ErrorHandler
        handlers.append((r"/(.*)", ErrorHandler))

        tornado.web.Application.__init__(self, handlers, **settings)

        self.forms = create_forms()

        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=settings.debug)
        self.db = scoped_session(sessionmaker(bind=engine))