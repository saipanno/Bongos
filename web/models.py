#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    models.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

from web import db

class PreDefinedOperate(db.Model):
    '''
    date:   time.strftime('%Y-%m-%d %H:%M')

    status: 0: wait to run
            1: running
            3: success
            4: fail
    '''

    __tablename__ = 'predefined_operate_list'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String, nullable=False)
    server_group = db.Column(db.UnicodeText, nullable=False)
    script_id = db.Column(db.UnicodeText, nullable=False)
    ssh_config = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, datetime, server_group, script_id, ssh_config):

        self.datetime   = datetime
        self.server_group  = server_group
        self.status = 0
        self.script_id  = script_id
        self.ssh_config = ssh_config

    def update_status(self, new_status):
        self.status = new_status

class CustomOperate(db.Model):
    '''
    date:   time.strftime('%Y-%m-%d %H:%M')

    status: 0: wait to run
            1: running
            3: success
            4: fail
    '''

    __tablename__ = 'custom_operate_list'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String)
    server_group = db.Column(db.UnicodeText)
    template_script = db.Column(db.UnicodeText)
    template_vars = db.Column(db.UnicodeText, default=None)
    ssh_config = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, datetime, server_group, template_script, ssh_config, template_vars=None):

        self.datetime   = datetime
        self.server_group  = server_group
        self.status = 0
        self.template_script  = template_script
        self.ssh_config = ssh_config
        if template_vars is not None:
            self.template_vars = template_vars

    def update_status(self, new_status):
        self.status = new_status


class PreDefinedScript(db.Model):
    __tablename__ = 'predefined_script_list'
    id   = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.UnicodeText)
    script = db.Column(db.UnicodeText)
    author = db.Column(db.UnicodeText)

    def __init__(self, desc, script, author):
        self.desc = desc
        self.script = script
        self.author = author


class SshConfig(db.Model):
    __tablename__ = 'ssh_config'
    id     = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.UnicodeText)
    ssh_port   = db.Column(db.Integer)
    ssh_user   = db.Column(db.Text)
    user_password = db.Column(db.Text)
    user_private_key  = db.Column(db.Text)


    def __init__(self, desc, ssh_user, user_password, ssh_port, user_private_key=None):
        self.desc = desc
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.user_password = user_password
        if user_private_key is not None:
            self.user_private_key  = user_private_key
