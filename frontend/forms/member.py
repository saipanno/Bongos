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


from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField

from frontend.models.member import Group


class UserLoginForm(Form):

    next_page = HiddenField()
    name = TextField()
    password = PasswordField()
    submit = SubmitField(u'Login', id='submit')


class CreateUserForm(Form):

    next_page = HiddenField()
    email = TextField(u'Email  <span class="required">*</span>', id='email', description=u'Unrepeatable')
    username = TextField(u'Username <span class="required">*</span>', id='name',
                         description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    group = QuerySelectField(u'Group  <span class="required">*</span>', id='group',
                             query_factory=Group.query.all, get_label='desc')
    password = PasswordField(u'Password  <span class="required">*</span>', id='password', description=u'At least eight')
    confirm_password = PasswordField(u'Confirm Password  <span class="required">*</span>',
                                     id='confirm_password', description=u'Re-enter the password')
    submit = SubmitField(u'Submit', id='submit')


class EditUserForm(Form):

    next_page = HiddenField()
    email = TextField(u'Email <span class="required">*</span>', id='email', description=u'Unrepeatable')
    username = TextField(u'Username <span class="required">*</span>', id='name',
                         description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    group = QuerySelectField(u'Group <span class="required">*</span>', id='group',
                             query_factory=Group.query.all, get_label='desc')
    now_password = PasswordField(u'Password  <span class="required">*</span>', id='password')
    new_password = PasswordField(u'New Password <span class="required">*</span>',
                                 id='new_password', description=u'At least eight')
    confirm_password = PasswordField(u'Confirm Password <span class="required">*</span>',
                                     id='confirm_password', description=u'Re-enter the new password')
    status = SelectField(u'Status  <span class="required">*</span>', id='status', choices=[(0, u'禁用'), (1, u'启用')])
    submit = SubmitField(u'Submit', id='submit')


class GroupForm(Form):

    next_page = HiddenField()
    name = TextField(u'Name <span class="required">*</span>', id='name',
                     description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    desc = TextField(u'Description <span class="required">*</span>', id='desc')
    submit = SubmitField(u'Submit', id='submit')