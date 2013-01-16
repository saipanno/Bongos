#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py, in Briseis.
#
#
# Created at 2013/01/12. Ruoyan Wong(@saipanno).


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

app.config.from_object('config')

from application.controllers.operate import mod as CreateScriptRunnerOperateCtrl
app.register_blueprint(CreateScriptRunnerOperateCtrl)