#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    settings.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

LOGIN_URL = '/login'

STATIC_PATH   = os.path.join(_basedir, 'static')
TEMPLATE_PATH = os.path.join(_basedir, 'templates')

XSRF_COOKIES = True
COOKIE_SECRET = 'nzjxcjasduuqwheazmu293nsadhaslzkci9023nsadnua9sdads/Vo='

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(_basedir), 'sqlite.db')