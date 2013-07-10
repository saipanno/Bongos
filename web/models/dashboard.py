#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/21.
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


from web.extensions.database import db


class SshConfig(db.Model):

    __tablename__ = 'ssh_config_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    port = db.Column(db.Integer)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    private_key = db.Column(db.String(50))

    def __init__(self, name, desc, port, username, password, private_key=None):
        self.name = name
        self.desc = desc
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key


class PreDefinedScript(db.Model):

    __tablename__ = 'predefined_script_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    script = db.Column(db.Text)
    author = db.Column(db.String(50))

    def __init__(self, name, desc, script, author):
        self.name = name
        self.desc = desc
        self.script = script
        self.author = author
