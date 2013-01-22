#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    detect.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, QuerySelectField

from web.models.base import SshConfig


class CreateSshDetectForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'address/hostname:', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    ssh_config = QuerySelectField(u'ssh login confg', id='select', description=u'ssh config', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Create', id='submit', description='submit')

class CreatePingDetectForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'address/hostname', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    submit = SubmitField(u'Create', id='submit', description='submit')