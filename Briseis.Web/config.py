#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Charon, An DataCenter Management.
#
#       config.py
#
#   Created at 2013/01/10. Ruoyan Wong(@saipanno).

import os

DEBUG = True

ROOT = os.path.abspath(os.getcwd())
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/database/charon.sqlite' % ROOT
BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_USE_CDN = True
BOOTSTRAP_FONTAWESOME = True
