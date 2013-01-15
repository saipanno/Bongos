#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    account.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import tornado.web

from website.handlers.base import *
from website.extensions.routing import route


@route(r'/login', name='login')
class Login(tornado.web.RequestHandler):
    def get(self):

        form = self.forms.LoginForm(next=self.get_args('next'))
        self.render('account/login.html', form=form)
        return