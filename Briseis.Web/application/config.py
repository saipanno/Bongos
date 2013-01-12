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

CSRF_ENABLED=True
CSRF_SESSION_KEY="SecretKeyForSessionSigning"