#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    base.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField


class UserLoginForm(Form):

    next = HiddenField()
    username = TextField(u'username', id='text')
    password = PasswordField(u'password', id='password')

    submit = SubmitField(u'login', id='submit', description='submit')