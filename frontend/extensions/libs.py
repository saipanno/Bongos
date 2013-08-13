#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/07/10.
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


import re
from flask.ext.wtf import ValidationError
from flask.ext.wtf import QuerySelectMultipleField as NativeQuerySelectMultipleField


def validate_address(address):

    try:
        octets = address.split('.')
        if len(octets) != 4:
            return False
        if int(octets[0]) == 127:
            return False
        for x in octets:
            if not (0 <= int(x) <= 255):
                return False
    except ValueError:
        return False
    return True


def format_address_list(address_list):

    """
    Returns an dict:
        {'status': True|False, 'desc': 'message'}
    Support sep:
        comma     (,)
        semicolon (;)
        blank     ( )
        newline   (\n)
    Result sep:
        String with blank sep.
    """

    try:
        new_address_list = str()
        for server in re.split(';|,| |\n', address_list):
            if server == u'':
                continue
            address_status = validate_address(server.strip())
            if address_status is not True:
                return {'status': False, 'desc': u'Incorrect IP address: %s' % server}
            new_address_list = '%s %s' % (new_address_list, server.strip())
    except Exception, e:
        return {'status': False, 'desc': u'%s' % e}

    return {'status': True, 'servers': u'%s' % new_address_list.strip()}


def format_ext_variables(ext_variables):

    address_vars_group = dict()

    for oneline in ext_variables.split('\n'):
        # 跳过ext_variables中的空行
        if oneline == u'':
            continue
        try:
            address = oneline.split('|')[0]
            if address == u'':
                return {'status': False, 'desc': u'Incorrect external variables: %s' % oneline}
            address_vars = oneline.split('|')[1]
            address_vars_group[address.strip()] = dict()
            for var in address_vars.split(','):
                try:
                    key = var.split('=')[0].strip()
                    if key == u'':
                        continue
                    value = var.split('=')[1].strip()
                    address_vars_group[address.strip()][key] = value
                except IndexError:
                    return {'status': False, 'desc': u'Incorrect external variables: %s' % oneline}
        except IndexError:
            return {'status': False, 'desc': u'Incorrect external variables: %s' % oneline}

    return {'status': True, 'vars': address_vars_group}


def catch_errors(errors):

    messages = ''

    if errors:
        for (field, errors) in errors.items():
            for error in errors:
                messages = '%s,%s' % (messages, error)

    return messages[1:] if messages else None


class QuerySelectMultipleField(NativeQuerySelectMultipleField):

    def iter_choices(self):
        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), obj.id in [o.id for o in self.data])


# WTForms Custom Validators
class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, attr, message=None):
        self.model = model
        self.attr = attr
        self.message = message if message else u'The current element value is already in use'

    def __call__(self, form, field):

        check = self.model.query.filter(self.attr == field.data).first()
        id = form.id.data if 'id' in form else None
        if check and (id is None or id != check.id):
            raise ValidationError('%s: %s' % (self.message, field.data))


class UnChange(object):
    """ validator that checks field unchange """
    field_flags = ('unchanged', )

    def __init__(self, model, attr, message=None):
        self.model = model
        self.attr = attr
        self.message = message if message else u'The current element can not be modified'

    def __call__(self, form, field):

        check = self.model.query.filter_by(id=form.id.data).first()
        if check is not None and field.data != getattr(check, self.attr):
            raise ValidationError('%s: %s' % (self.message, field.data))


class UnChanged(object):
    """ validator that checks field unchange """
    field_flags = ('unchanged', )

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


class Depend(object):
    """ validator that checks field depend on """
    def __init__(self, attr, message=None):
        self.attr = attr
        self.message = message if message else u'Dependent setting does not exist'

    def __call__(self, form, field):

        if hasattr(form, self.attr) and not getattr(form, self.attr).data:
            raise ValidationError(self.message)


def get_obj_attributes(obj, key_header):

    fruit = dict()
    fruit['%s_ID' % key_header.upper()] = obj.id
    for key in obj.__dict__.keys():
        if key.startswith('_') is not True:
            fruit['%s_%s' % (key_header.upper(), key.upper())] = obj.__dict__[key]

    return fruit


def get_dict_items(obj, key_header):

    fruit = dict()
    for key in obj:
        fruit['%s_%s' % (key_header.upper(), key.upper())] = obj[key]

    return fruit