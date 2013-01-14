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
from website.extensions import *
from website.extensions.routing import Route


class Application(tornado.web.Application):

    def __init__(self):
        settings = config_from_object(config)

        handlers = [
            # other handlers...
            url(r"/theme/(.+)", tornado.web.StaticFileHandler, dict(path=settings['theme_path']), name='theme_path'),
            url(r"/upload/(.+)", tornado.web.StaticFileHandler, dict(path=settings['upload_path']), name='upload_path')
        ]

        # Custom 404 ErrorHandler
        handlers.append((r"/(.*)", ErrorHandler))

        tornado.web.Application.__init__(self, handlers, **settings)