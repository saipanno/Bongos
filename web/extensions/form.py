#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    form.py, in Briseis.
#
#
#    Created at 2013/01/15. Ruoyan Wong(@saipanno).

import re

from wtforms import Form as BaseForm, fields, validators, widgets, ext

from wtforms.fields import BooleanField, DecimalField, DateField,\
    DateTimeField, FieldList, FloatField, FormField,\
    HiddenField, IntegerField, PasswordField, RadioField, SelectField,\
    SelectMultipleField, SubmitField, TextField, TextAreaField

from wtforms.validators import ValidationError, Email, email, EqualTo, equal_to,\
    IPAddress, ip_address, Length, length, NumberRange, number_range,\
    Optional, optional, Required, required, Regexp, regexp,\
    URL, url, AnyOf, any_of, NoneOf, none_of

from wtforms.widgets import CheckboxInput, FileInput, HiddenInput,\
    ListWidget, PasswordInput, RadioInput, Select, SubmitInput,\
    TableWidget, TextArea, TextInput



class Form(BaseForm):

    def __init__(self, formdata=None, *args, **kwargs):
        self.obj = kwargs.get('obj', None)
        super(Form, self).__init__(formdata, *args, **kwargs)


    def hidden_tag(self, *fields):
        """
        Wraps hidden fields in a hidden DIV tag, in order to keep XHTML
        compliance.
        """

        if not fields:
            fields = [f for f in self if isinstance(f, HiddenField)]

        rv = []
        for field in fields:
            if isinstance(field, basestring):
                field = getattr(self, field)
            rv.append(unicode(field))

        return u"".join(rv)