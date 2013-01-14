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

from website.helper import config_from_object
from website.extensions.routing import Route


class Application(tornado.web.Application):

    def __init__(self):
        settings = config_from_object(config)

        handlers = [
            (r'/login', IndexHandler),
            (r'/operate/show', IndexHandler),
            (r'/operate/query', IndexHandler),
            (r'/operate/create', IndexHandler),
            (r'/', IndexHandler)
        ] + Route.get_routes()

        # Custom 404 ErrorHandler
        handlers.append((r"/(.*)", ErrorHandler))

        tornado.web.Application.__init__(self, handlers, **settings)