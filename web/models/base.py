#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    base.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

from web import db


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
        self.user_private_key  = user_private_key
