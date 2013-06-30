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


from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField


class UserLoginForm(Form):

    next_page = HiddenField()
    email = TextField(u'Email:', id='email')
    password = PasswordField(u'Password:', id='password')
    submit = SubmitField(u'Login', id='submit')


class CreateUserForm(Form):

    next_page = HiddenField()
    email = TextField(u'Email<span class="required">*</span>', id='email', description=u'Required.')
    username = TextField(u'Username<span class="required">*</span>', id='text', description=u'Required.')
    password = PasswordField(u'Password<span class="required">*</span>', id='password', description=u'Required.')
    confirm_password = PasswordField(u'Repeat Password<span class="required">*</span>', id='confirm_password',
                                     description=u'Required.')
    submit = SubmitField(u'Save', id='submit')


class EditUserForm(Form):

    next_page = HiddenField()
    email = TextField(u'Email<span class="required">*</span>', id='email', description=u'Required.')
    username = TextField(u'Username<span class="required">*</span>', id='text', description=u'Required.')
    now_password = PasswordField(u'Now Password<span class="required">*</span>', id='now_password',
                                 description=u'Now Password')
    new_password = PasswordField(u'New Password<span class="required">*</span>', id='new_password',
                                 description=u'New Password You Want.')
    confirm_password = PasswordField(u'Repeat New Password<span class="required">*</span>', id='confirm_password',
                                     description=u'Repeat New Password to Confirm.')
    submit = SubmitField(u'Save', id='submit')