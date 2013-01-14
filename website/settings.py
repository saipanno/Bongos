#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    settings.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

import os

DEBUG = True

LOGIN_URL = '/login'

STATIC_PATH   = os.path.join(os.path.dirname(__file__), 'static')
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
