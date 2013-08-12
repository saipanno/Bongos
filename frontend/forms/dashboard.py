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


from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, IntegerField, HiddenField, HiddenInput,\
    PasswordField, BooleanField, QuerySelectMultipleField
from flask.ext.wtf import Required, Optional, Regexp, Email

from frontend.models.account import Group, User
from frontend.models.dashboard import SshConfig, IpmiConfig, FabFile

from frontend.extensions.libs import Unique, UnChanged


class SshConfigForm(Form):

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    name = TextField(u'Name', description=u'Ssh Config name. Unique',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 Unique(SshConfig, SshConfig.name,
                                        message=u'The current name is already in use')])
    desc = TextField(u'Description', validators=[Required(message=u'Description is required')])
    port = IntegerField(u'Port', default=22,
                        validators=[Required(message=u'Port is required')])
    username = TextField(u'Username', default=u'root',
                         validators=[Required(message=u'Username is required')])
    password = PasswordField(u'Password',
                             validators=[Required(message=u'Password is required')])
    private_key = TextField(u'Private Key:',
                            description=u'Private filename in <code>PRIVATE_KEY_PATH</code>')

    submit = SubmitField(u'Submit', id='submit')


class IpmiConfigForm(Form):

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    name = TextField(u'Name', description=u'Ipmi Config name. Unique',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 Unique(IpmiConfig, IpmiConfig.name,
                                        message=u'The current name is already in use')])
    desc = TextField(u'Description', validators=[Required(message=u'Description is required')])
    username = TextField(u'Username', default=u'root',
                         validators=[Required(message=u'Username is required')])
    password = PasswordField(u'Password',
                             validators=[Required(message=u'Password is required')])
    interface = BooleanField(u'IPMI Interface:',
                             description=u'Select to use <code>lanplus</code> interface, default is <code>lan</code>.')

    submit = SubmitField(u'Submit', id='submit')


class CreateUserForm(Form):

    # TODO: NAME字段格式检查的中文支持

    next_page = HiddenField()

    email = TextField(u'Email', description=u'Unique',
                      validators=[Required(message=u'Email is required'),
                                  Email(message=u'Incorrect email format'),
                                  Unique(User, User.email, message=u'The current email is already in use')])
    username = TextField(u'Username', description=u'Unique',
                         validators=[Required(message=u'Username is required'),
                                     Regexp(u'^[a-zA-Z0-9\_\-\.]{5,20}$', message=u'Incorrect username format'),
                                     Unique(User, User.username, message=u'The current name is already in use')])
    name = TextField(u'Name', description=u'Unique',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 Unique(User, User.name, message=u'The current name is already in use')])
    groups = QuerySelectMultipleField(u'Group', description=u'Multiple Choice',
                                      query_factory=Group.query.all, get_label='desc',
                                      validators=[Required(message=u'Group is required')])
    password = TextField(u'Password', description=u'At least five characters',
                         validators=[Required(message=u'Password is required'),
                                     Regexp(u'^.{5,20}$', message=u'Password are at least five chars')])
    status = BooleanField(u'Status', description=u'Check to enable this user')

    submit = SubmitField(u'Submit', id='submit')


class EditUserForm(Form):

    # TODO: NAME字段格式检查的中文支持

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    email = TextField(u'Email', validators=[UnChanged()])
    username = TextField(u'Username', validators=[UnChanged()])
    name = TextField(u'Name', description=u'Unique',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 Unique(User, User.name, message=u'The current name is already in use')])
    groups = QuerySelectMultipleField(u'Group', description=u'Multiple Choice',
                                      query_factory=Group.query.all, get_label='desc',
                                      validators=[Required(message=u'Group is required')])
    password = TextField(u'Password', description=u'At least five characters',
                         validators=[Optional(),
                                     Regexp(u'^.{5,20}$', message=u'Password are at least five chars')])

    submit = SubmitField(u'Submit', id='submit')


class FabFileForm(Form):

    script_desc = u'''作为shell中的 <code>$</code> 内部变量的扩展，模板还支持外部变量。\
    <code>{{</code> 和 <code>}}</code> 作为外部变量的定界符,此类变量会依据变量文件中的同名赋值定义进行替换, \
    同时标准错误输出以及标准输出中匹配到<code>BD:\w+?:EOF</code>的字符串可以作为返回结果保存。如：
<code>device=eth1; echo "IPADDR={{address}}"  >> ~/ifcfg-$device</code>'''

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    name = TextField(u'Name', description=u'Fabfile name. Unique',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_]{5,50}$', message=u'Incorrect name format'),
                                 Unique(FabFile, FabFile.name,
                                        message=u'The current name is already in use')])
    desc = TextField(u'Description', validators=[Required(message=u'Description is required')])
    script = TextAreaField(u'Fabfile', description=u'Fabric\'s fabfile')

    submit = SubmitField(u'Submit', id='submit')