#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    detect.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

from web import db


class SshDetect(db.Model):
    '''
    date:   time.strftime('%Y-%m-%d %H:%M')

    status: 0: wait
            1: running
            3: success
            4: fail
    '''

    __tablename__ = 'ssh_detect_list'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.UnicodeText, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    server_list = db.Column(db.UnicodeText, nullable=False)
    ssh_config = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, author, datetime, server_list, ssh_config):

        self.author = author
        self.datetime = datetime
        self.server_list = server_list
        self.status = 0
        self.ssh_config = ssh_config

    def update_status(self, new_status):
        self.status = new_status


class PingDetect(db.Model):
    '''
    date:   time.strftime('%Y-%m-%d %H:%M')

    status: 0: wait
            1: running
            3: success
            4: fail
    '''

    __tablename__ = 'ping_detect_list'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.UnicodeText, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    server_list = db.Column(db.UnicodeText, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, author, datetime, server_list):

        self.author = author
        self.datetime = datetime
        self.server_list = server_list
        self.status = 0

    def update_status(self, new_status):
        self.status = new_status
