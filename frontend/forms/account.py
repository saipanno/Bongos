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


from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, IntegerField, HiddenInput
from flask.ext.wtf import Required, EqualTo, Regexp, Optional

from frontend.models.account import User, Group

from frontend.extensions.utility import Unique, UnChange, Depend


class UserLoginForm(Form):

    next_page = HiddenField()

    key_name = TextField(u'Username or Email',
                         validators=[Required(message=u'Username or Email is required')])
    password = PasswordField(u'Password',
                             validators=[Required(message=u'Password is required')])

    submit = SubmitField(u'Login', id='submit')


class EditSettingForm(Form):

    # TODO: NAME字段格式检查的中文支持

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    email = TextField(u'Email', description=u'Can not be modified',
                      validators=[UnChange(User, 'email', message=u'The current email can not be modified')])
    username = TextField(u'Username', description=u'Can not be modified',
                         validators=[UnChange(User, 'username', message=u'The current username can not be modified')])
    name = TextField(u'Name', description=u'Unique',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 Unique(User, User.name, message=u'The current name is already in use')])

    now_password = PasswordField(u'Password')
    new_password = PasswordField(u'New Password', description=u'At least eight characters',
                                 validators=[Optional(),
                                             Regexp(u'(^.{8,20}$)|(^$)', message=u'Password are at least eight chars'),
                                             Depend('now_password',
                                                    message=u'Password is required when changing password')])
    confirm_password = PasswordField(u'Confirm Password', description=u'Re-enter the new password',
                                     validators=[Optional(),
                                                 EqualTo('new_password', message=u'New passwords must be the same')])

    submit = SubmitField(u'Submit', id='submit')


class GroupForm(Form):

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    name = TextField(u'Name', description=u'Unique',
                     validators=[Required(message=u'Name is required'),
                                 Unique(Group, Group.name, message=u'The current name is already in use')])
    desc = TextField(u'Description', validators=[Required(message=u'Description is required')])

    submit = SubmitField(u'Submit', id='submit')