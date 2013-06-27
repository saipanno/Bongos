#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/24.
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


from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, IntegerField


class CreatePreDefinedScriptForm(Form):

    name = TextField(u'脚本名称:', id='text', description=u'脚本名称', default=u'')
    desc = TextAreaField(u'脚本描述:', id='text', description=u'脚本描述', default=u'')
    script = TextAreaField(u'脚本/脚本模板:', id='textarea', description=u'预定义脚本,支持模板功能', default=u'')
    submit = SubmitField(u'Continue', id='submit', description='submit')


class CreateSshConfigForm(Form):

    name = TextField(u'SSH配置名称:', id='text', description=u'配置名称', default=u'')
    desc = TextField(u'SSH配置描述:', id='text', description=u'配置描述', default=u'')
    port = IntegerField(u'SSH端口:', id='port', description=u'SSH端口', default=22)
    username = TextField(u'SSH用户名:', id='text', description=u'SSH用户名', default=u'')
    password = TextField(u'SSH密码:', id='text', description=u'SSH密码', default=u'')
    key_filename = TextField(u'SSH密钥:', id='text', description=u'SSH密钥', default=u'')
    submit = SubmitField(u'Continue', id='submit', description='submit')