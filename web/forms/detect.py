#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/16.
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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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