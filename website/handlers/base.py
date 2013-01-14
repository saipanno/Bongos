#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    base.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import os
import logging

import tornado.web
import tornado.locale
import tornado.escape
import tornado.ioloop

# from website.extensions.sessions import Session

class ErrorHandler(tornado.web.RequestHandler):
    """raise 404 error if url is not found.
    fixed tornado.web.RequestHandler HTTPError bug.
    """
    def prepare(self):
        self.set_status(404)
        raise tornado.web.HTTPError(404)