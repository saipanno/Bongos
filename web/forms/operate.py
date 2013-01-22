#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    operate.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, QuerySelectField

from web.models.base import SshConfig
from web.models.operate import PreDefinedScript


class CreatePreDefinedOperateForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'Address:', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    script_list = QuerySelectField(u'PreDefined Script:', id='select', description=u'PreDefined Script', query_factory=PreDefinedScript.query.all,  get_label='desc')
    ssh_config = QuerySelectField(u'ssh login confg', id='select', description=u'ssh config', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Create', id='submit', description='submit')

class CreateCustomOperateForm(Form):


    next = HiddenField()
    server_list = TextAreaField(u'address/hostname', id='textarea', description=u'server you want to operated, support address or hostname.', default=u'None')
    template_script = TextAreaField(u'template script', id='textarea', description=u'select script from given list.', default=u'None')
    template_vars = TextAreaField(u'template vars', id='textarea', description=u'var list.', default=u'None')
    ssh_config = QuerySelectField(u'ssh login confg', id='select', description=u'ssh config', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Create', id='submit', description='submit')