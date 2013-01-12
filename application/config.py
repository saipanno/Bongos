#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Charon, An DataCenter Management.
#
#       config.py
#
#   Created at 2013/01/10. Ruoyan Wong(@saipanno).

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'sqlite.db')
DATABASE_CONNECT_OPTIONS = {}

APPLICATION_ROOT = '/Users/saipanno/Projects/Briseis'

CSRF_ENABLED = True
SECRET_KEY = '4bt!\t\x97\xde\xa5R\xfbu\xc0\xe5\x8f\xe0Fz\x00\xa2P\x8d\x85\x97\x08'