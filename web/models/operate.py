#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/16.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from web import db


class PreDefinedOperate(db.Model):
    '''
    date:   time.strftime('%Y-%m-%d %H:%M')

    status: 0: wait
            1: running
            3: success
            4: fail
    '''

    __tablename__ = 'predefined_operate_list'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.UnicodeText, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    server_list = db.Column(db.UnicodeText, nullable=False)
    script_id = db.Column(db.UnicodeText, nullable=False)
    template_vars = db.Column(db.UnicodeText, default=None)
    ssh_config = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, author, datetime, server_list, script_id, template_vars, ssh_config):

        self.author = author
        self.datetime = datetime
        self.server_list = server_list
        self.status = 0
        self.script_id = script_id
        self.ssh_config = ssh_config
        self.template_vars = template_vars

    def update_status(self, new_status):
        self.status = new_status

class CustomOperate(db.Model):
    '''
    date:   time.strftime('%Y-%m-%d %H:%M')

    status: 0: wait
            1: running
            3: success
            4: fail
    '''

    __tablename__ = 'custom_operate_list'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.UnicodeText, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    server_list = db.Column(db.UnicodeText, nullable=False)
    template_script = db.Column(db.UnicodeText, nullable=False)
    template_vars = db.Column(db.UnicodeText, default=None)
    ssh_config = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, author, datetime, server_list, template_script, template_vars, ssh_config):

        self.author = author
        self.datetime = datetime
        self.server_list  = server_list
        self.status = 0
        self.template_script  = template_script
        self.ssh_config = ssh_config
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