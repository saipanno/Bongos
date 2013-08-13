#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/08/04.
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


from flask.ext.wtf import Form, TextField, SubmitField, IntegerField, HiddenField, HiddenInput,\
    QuerySelectField
from flask.ext.wtf import Required, Optional, Regexp, IPAddress

from frontend.models.account import Group
from frontend.models.assets import Server, IDC

from frontend.extensions.libs import Unique, QuerySelectMultipleField


class ServerForm(Form):

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    serial_number = TextField(u'Serial Number', description=u'Unique',
                              validators=[Optional(),
                                          Unique(Server, Server.serial_number,
                                                 message=u'The current serial number is already in use')])
    assets_number = TextField(u'Assets Number', description=u'Unique',
                              validators=[Optional(),
                                          Unique(Server, Server.assets_number,
                                                 message=u'The current assets number is already in use')])
    groups = QuerySelectMultipleField(u'Group', description=u'Multiple Choice',
                                      query_factory=Group.query.all, get_label='desc',
                                      validators=[Required(message=u'Group is required')])
    desc = TextField(u'Server Description')
    ext_address = TextField(u'Ext Address', description=u'Unique',
                            validators=[Optional(),
                                        IPAddress(message=u'Incorrect ip address format'),
                                        Unique(Server, Server.ext_address,
                                               message=u'The current ext address is already in use')])
    int_address = TextField(u'Int Address', description=u'Unique',
                            validators=[Optional(),
                                        IPAddress(message=u'Incorrect ip address format'),
                                        Unique(Server, Server.int_address,
                                               message=u'The current int address is already in use')])
    ipmi_address = TextField(u'IPMI Address', description=u'Unique',
                             validators=[Optional(),
                                         IPAddress(message=u'Incorrect ip address format'),
                                         Unique(Server, Server.ipmi_address,
                                                message=u'The current ipmi address is already in use')])
    other_address = TextField(u'Other Address',
                              description=u'Other Address, split by <code>,</code>')
    idc = QuerySelectField(u'IDC', query_factory=IDC.query.all, get_label='name',
                           validators=[Required(message=u'IDC is required')])
    rack = TextField(u'Rack', description=u'Unique',
                     validators=[Required(message=u'Rack is required'),
                                 Unique(Server, Server.rack,
                                        message=u'The current rack is already in use')])
    manufacturer = TextField(u'Manufacturer')
    model = TextField(u'Model')
    cpu_info = TextField(u'Cpu Model')
    disk_info = TextField(u'Disk Information')
    memory_info = TextField(u'Memory Information')

    submit = SubmitField(u'Submit', id='submit')


class IDCForm(Form):

    next_page = HiddenField()
    id = IntegerField(widget=HiddenInput())

    name = TextField(u'Name', validators=[Required(message=u'Name is required'),
                                          Regexp(u'^[a-zA-Z0-9\_\-\.]{3,20}$', message=u'Incorrect name format')])
    desc = TextField(u'Description', validators=[Required(message=u'Description is required')])
    operators = TextField(u'Operators', validators=[Required(message=u'Operators is required')])
    address = TextField(u'Address', validators=[Required(message=u'Address is required')])

    submit = SubmitField(u'Submit', id='submit')
