#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

import tornado.web
import tornado.locale

from website import settings as config

from website.helper import import_setting_from_config
from website.forms import create_forms
from website.extensions.routing import route


from website.handlers.base import ErrorHandler

class Application(tornado.web.Application):

    def __init__(self):
        settings = import_setting_from_config(config)

        handlers = route.get_routes()

        # Custom 404 ErrorHandler
        handlers.append((r"/(.*)", ErrorHandler))

        tornado.web.Application.__init__(self, handlers, **settings)

        self.forms = create_forms()