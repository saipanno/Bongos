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


from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, QuerySelectField

from web.models.base import SshConfig


class CreateSshDetectForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'服务器列表:', id='textarea', description=u'支持域名或IP地址,一行一个.', default=u'None')
    ssh_config = QuerySelectField(u'SSH配置:', id='select', description=u'SSH配置.包含SSH端口,用户名,密码以及密钥(可选).', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Continue', id='submit')

class CreatePingDetectForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'服务器列表:', id='textarea', description=u'支持域名或IP地址,一行一个.', default=u'None')
    submit = SubmitField(u'Continue', id='submit')