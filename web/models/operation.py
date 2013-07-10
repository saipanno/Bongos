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


from web.extensions.database import db


class OperationDb(db.Model):

    """
    DATE:   time.strftime('%Y-%m-%d %H:%M')
    STATUS: 0: 队列中
            1: 成功
            2: 错误
            5: 执行中
            other: 异常错误

    """

    __tablename__ = 'operation_lists'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    datetime = db.Column(db.String(50))
    kind = db.Column(db.String(25))
    server_list = db.Column(db.Text)
    script_template = db.Column(db.Text)
    template_vars = db.Column(db.Text)
    ssh_config = db.Column(db.Integer)
    status = db.Column(db.Integer)
    result = db.Column(db.Text)

    def __init__(self, author, datetime, kind, server_list, script_template, template_vars, ssh_config, status, result):

        self.author = author
        self.datetime = datetime
        self.kind = kind
        self.server_list = server_list
        self.script_template = script_template
        self.ssh_config = ssh_config
        self.template_vars = template_vars
        self.status = status
        self.result = result