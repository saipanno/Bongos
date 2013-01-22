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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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
