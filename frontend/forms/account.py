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


from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField, \
    Required, EqualTo, Regexp

from frontend.models.account import Group


class UserLoginForm(Form):

    next_page = HiddenField()
    key_name = TextField(u'Username or Email',
                         validators=[Required(message=u'Username or Email is required')])
    password = PasswordField(u'Password',
                             validators=[Required(message=u'Password is required')])
    submit = SubmitField(u'Login', id='submit')


class CreateUserForm(Form):

    next_page = HiddenField()
    email = TextField(u'Email', description=u'Unrepeatable')
    username = TextField(u'Username', description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    name = TextField(u'Name', description=u'Unrepeatable.')
    group = QuerySelectField(u'Group', query_factory=Group.query.all, get_label='desc')
    password = PasswordField(u'Password', description=u'At least eight')
    confirm_password = PasswordField(u'Confirm Password',
                                     validators=[EqualTo('password', message=u'error confirm password')],
                                     id='confirm_password', description=u'Re-enter the password')
    submit = SubmitField(u'Submit', id='submit')


class EditUserForm(Form):

    # TODO: NAME字段格式检查的中文支持

    next_page = HiddenField()
    email = TextField(u'Email', description=u'Can not be modified',
                      validators=[Required(message=u'Username or Email is required')])
    username = TextField(u'Username', description=u'Can not be modified',
                         validators=[Required(message=u'Password is required')])
    name = TextField(u'Name', description=u'Unrepeatable.',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format')])
    group = QuerySelectField(u'Group', description=u'',
                             query_factory=Group.query.all, get_label='desc',
                             validators=[Required(message=u'Group is required')])
    now_password = PasswordField(u'Password')
    new_password = PasswordField(u'New Password', description=u'At least eight characters',
                                 validators=[Regexp(u'^.{8,20}$', message=u'Password are at least eight characters')])
    confirm_password = PasswordField(u'Confirm Password', description=u'Re-enter the new password',
                                     validators=[EqualTo('new_password', message=u'New passwords must be the same')])
    status = SelectField(u'Status', description=u'Enable or Disable User',
                         choices=[(0, u'Disable'), (1, u'Enable')],
                         validators=[Required(message=u'User status is required')])
    submit = SubmitField(u'Save', id='submit')


class GroupForm(Form):

    next_page = HiddenField()
    name = TextField(u'Name', description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    desc = TextField(u'Description')
    submit = SubmitField(u'Save', id='submit')