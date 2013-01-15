#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    forms.py, in Briseis.
#
#
#    Created at 2013/01/15. Ruoyan Wong(@saipanno).

from web.extensions.form import Form, TextField, PasswordField, SubmitField,\
    TextAreaField, BooleanField, HiddenField, ValidationError,\
    required, regexp, equal_to, email, optional, url

USERNAME_RE = r'^[\w.+-]+$'

def create_forms():

    is_username = regexp(USERNAME_RE,
                        message="You can only use letters, numbers or dashes")

    class FormWrapper(object):

        class LoginForm(Form):
            login = TextField("Username or email", validators=[
                    required(message="You must provide an email or username")])

            password = PasswordField("Password")

            remember = BooleanField("Remember me")

            next = HiddenField()

            submit = SubmitField("Login")

    return FormWrapper
