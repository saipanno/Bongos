#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    __init__.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SECRET_KEY'] = '4bt!\t\x97\xde\xa5R\xfbu\xc0\xe5\x8f\xe0Fz\x00\xa2P\x8d\x85\x97\x08'

db = SQLAlchemy(app)

from application.controllers.operate import mod as CreateScriptRunnerOperateCtrl
app.register_blueprint(CreateScriptRunnerOperateCtrl)