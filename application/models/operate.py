#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    create.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

from application import db

class CreateScriptRunnerOperate(db.Model):
    __tablename__ = 'operate_list'
    id = db.Column(db.Integer, primary_key=True)
    operate_type   = db.Column(db.Integer)
    server_list    = db.Column(db.UnicodeText)
    command_list   = db.Column(db.UnicodeText)
    variable_list  = db.Column(db.UnicodeText)
    operate_status = db.Column(db.Integer)

    def __init__(self, operate_type, server_list, command_list, variable_list, operate_status=False):
        self.operate_type   = operate_type
        self.server_list    = server_list
        self.command_list   = command_list
        self.variable_list  = variable_list
        self.operate_status = operate_status
