#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    models.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

from web import db

class CreateOperateRunner(db.Model):
    __tablename__ = 'operate_list'
    id     = db.Column(db.Integer, primary_key=True)
    type   = db.Column(db.Integer)
    server = db.Column(db.UnicodeText)
    script = db.Column(db.UnicodeText)
    var    = db.Column(db.UnicodeText)
    status = db.Column(db.Integer)

    def __init__(self, type, server, script, var='', status=0):
        self.type = type
        self.server = server
        self.script = script
        self.var    = var
        self.status = status