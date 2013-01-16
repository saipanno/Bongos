#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    model.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import tornado.web
import tornado.escape

from web.extensions.routing import route

class BaseRequestHandler(tornado.web.RequestHandler):

    @property
    def forms(self):
        return self.application.forms

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_json = self.get_secure_cookie('user')
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)


class ErrorHandler(BaseRequestHandler):

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code, 'oops~ expect an 404.')


@route('/login')
class AuthLoginHandler(BaseRequestHandler):

    def get(self):

        form = self.forms.LoginForm(next=self.get_arguments('next'))
        self.render('login.html', form=form)

    def post(self, *args, **kwargs):

        form = self.forms.LoginForm(next=self.get_arguments('next'))
        if form.validate():
            pass

class AuthLogoutHandler(BaseRequestHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))