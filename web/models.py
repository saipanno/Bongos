#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    models.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

from web import db

class OperateList(db.Model):
    __tablename__ = 'operate_list'
    id     = db.Column(db.Integer, primary_key=True)
    date   = db.Column(db.DateTime)
    type   = db.Column(db.Integer)
    server = db.Column(db.UnicodeText)
    script = db.Column(db.Integer)
    var    = db.Column(db.UnicodeText)
    ssh_config = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, type, date, server, script, var='', ssh_config=0):
        self.type = type
        self.date = date
        self.server = server
        self.script = script
        self.var    = var
        self.ssh_config = ssh_config
        self.status = 0


class RemoteScript(db.Model):
    __tablename__ = 'remote_script'
    id   = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    script = db.Column(db.UnicodeText)
    var    = db.Column(db.UnicodeText)

    def __init__(self, type, script, var=''):
        self.type = type
        self.script = script
        self.var  = var

class SshConfig(db.Model):
    __tablename__ = 'ssh_config'
    id     = db.Column(db.Integer, primary_key=True)
    user   = db.Column(db.Text)
    password = db.Column(db.Text)
    private  = db.Column(db.Text)
    port   = db.Column(db.Integer)

    def __init__(self, user, password, port, private='None'):
        self.user = user
        self.password = password
        self.private  = private
        self.port = port