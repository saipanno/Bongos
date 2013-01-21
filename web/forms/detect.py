#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    detect.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, SelectField


class CreateSshDetectForm(Form):

    ssh_configs = [(1, u'ku6.com'), (2, u'snda.com'), (3, u'saipanno.com')]

    next = HiddenField()
    server_list = TextAreaField(u'address/hostname:', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    ssh_config = SelectField(u'ssh_confg', id='select', choices=ssh_configs, description=u'ssh config', default=u'None')
    submit = SubmitField(u'Create', id='submit', description='submit')

class CreatePingDetectForm(Form):

    ssh_configs = [(1, u'ku6.com'), (2, u'snda.com'), (3, u'saipanno.com')]

    next = HiddenField()
    server_list = TextAreaField(u'address/hostname', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    submit = SubmitField(u'Create', id='submit', description='submit')