#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    settings.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

PORT = 80
HOST = '0.0.0.0'

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'sqlite.db')

SECRET_KEY = '4bt!\t\x97\xde\xa5R\xfbu\xc0\xe5\x8f\xe0Fz\x00\xa2P\x8d\x85\x97\x08'
