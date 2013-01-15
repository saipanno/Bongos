#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    models.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import tornado.web

from web.extensions.routing import route


class BaseRequestHandler(tornado.web.RequestHandler):

    @property
    def forms(self):
        return self.application.forms[self.locale.code]

@route('/login')
class LoginHandler(BaseRequestHandler):

    def get(self):

        form = self.forms.LoginForm(next=self.get_arguments('next'))
        self.render('login.html', form=form)

    def post(self, *args, **kwargs):
        self.render('show_fucking.html', fucking=str(self.request.headers))