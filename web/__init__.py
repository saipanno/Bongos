#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py, in Briseis.
#
#
# Created at 2013/01/12. Ruoyan Wong(@saipanno).

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from web.views import base
from web.views import detect
from web.views import operate
