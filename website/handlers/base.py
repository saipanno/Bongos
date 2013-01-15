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


from website.extensions.routing import route


class BaseRequestHandler(tornado.web.RequestHandler):

    @property
    def forms(self):
        return self.application.forms


class ErrorHandler(BaseRequestHandler):
    """raise 404 error if url is not found.
    fixed tornado.web.RequestHandler HTTPError bug.
    """
    def prepare(self):
        self.set_status(404)
        raise tornado.web.HTTPError(404)


@route('/login')
class LoginHandler(BaseRequestHandler):

    def get(self):

        form = self.forms.LoginForm(next=self.get_arguments('next'))
        self.render('login.html', form=form)

    def post(self, *args, **kwargs):
        self.render('show_fucking.html', fucking=str(self.request.headers))