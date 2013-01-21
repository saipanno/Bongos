#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    operate.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

from flask.ext.wtf import Form, TextField, TextAreaField, HiddenField, SubmitField, SelectField, PasswordField


class CreatePreDefinedOperateForm(Form):

    ssh_configs = [(1, u'ku6.com'), (2, u'snda.com'), (3, u'saipanno.com')]
    script_choices = [(1, u'CDN User Initialize'), (2, u'CDN CentOS Initialize'), (3, u'CDN DNS Update'), (4, u'Server Reboot'), (5, u'Server Shutdown')]

    next = HiddenField()
    server_list = TextAreaField(u'address/hostname:', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    script_id = SelectField(u'script', id='select', choices=script_choices, description=u'select script from given list.', default=u'None')
    ssh_config = SelectField(u'ssh_confg', id='select', choices=ssh_configs, description=u'ssh config', default=u'None')
    submit = SubmitField(u'Create', id='submit', description='submit')

class CreateCustomOperateForm(Form):

    ssh_configs = [(1, u'ku6.com'), (2, u'snda.com'), (3, u'saipanno.com')]

    next = HiddenField()
    server_list = TextAreaField(u'address/hostname', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    template_script = TextAreaField(u'template script', id='textarea', description=u'select script from given list.', default=u'None')
    template_vars = TextAreaField(u'template vars', id='textarea', description=u'var list.', default=u'None')
    ssh_config = SelectField(u'ssh login confg', id='select', choices=ssh_configs, description=u'ssh config', default=u'None')
    submit = SubmitField(u'Create', id='submit', description='submit')