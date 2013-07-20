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


from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, IntegerField, \
    PasswordField, QuerySelectField, BooleanField

from frontend.models.member import Group
from frontend.models.dashboard import AccessControl


class CreatePreDefinedScriptForm(Form):

    script_desc = u'''作为shell中的 <code>$</code> 内部变量的扩展，模板还支持外部变量。\
    <code>{{</code> 和 <code>}}</code> 作为外部变量的定界符,此类变量会依据变量文件中的同名赋值定义进行替换, \
    同时标准错误输出以及标准输出中匹配到<code>BD:\w+?:EOF</code>的字符串可以作为返回结果保存。如：
<code>device=eth1; echo "IPADDR={{address}}"  >> ~/ifcfg-$device</code>'''

    name = TextField(u'Name  <span class="required">*</span>', id='text',
                     description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    desc = TextField(u'Description  <span class="required">*</span>', id='text')
    script = TextAreaField(u'Script  <span class="required">*</span>', id='textarea', description=script_desc)
    submit = SubmitField(u'Submit', id='submit')


class CreateSshConfigForm(Form):

    name = TextField(u'Name  <span class="required">*</span>', id='text',
                     description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    desc = TextField(u'Description  <span class="required">*</span>', id='text')
    port = IntegerField(u'Port  <span class="required">*</span>', id='port', default=22)
    username = TextField(u'Username  <span class="required">*</span>', id='text', default=u'root')
    password = PasswordField(u'Password  <span class="required">*</span>', id='text')
    private_key = TextField(u'Private Key:', id='text',
                            description=u'Private key filename, not required.')
    submit = SubmitField(u'Submit', id='submit')


class ServerForm(Form):

    group = QuerySelectField(u'Group  <span class="required">*</span>', id='group',
                             query_factory=Group.query.all, get_label='desc')
    desc = TextField(u'Server Desc', id='text')
    ext_address = TextField(u'Ext Address', id='text')
    int_address = TextField(u'Int Address', id='text')
    ipmi_address = TextField(u'IPMI Address', id='text')
    other_address = TextField(u'Other Address', id='text')
    idc = TextField(u'IDC', id='text')
    rack = TextField(u'Rack', id='text')
    manufacturer = TextField(u'Manufacturer', id='text')
    model = TextField(u'Model', id='text')
    cpu_info = TextField(u'Cpu Model', id='text')
    disk_info = TextField(u'Disk Information', id='text')
    memory_info = TextField(u'Memory Information', id='text')

    submit = SubmitField(u'Submit', id='submit')


class AccessControlForm(Form):

    name = QuerySelectField(u'Function  <span class="required">*</span>',
                            query_factory=AccessControl.query.all, get_label='function')

    group = QuerySelectField(u'Group  <span class="required">*</span>',
                             query_factory=Group.query.all, get_label='desc')

    permission = BooleanField(u'Permission  <span class="required">*</span>', default=False)

    submit = SubmitField(u'Submit', id='submit')