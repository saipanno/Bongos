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


NAME_REGEX = u'^[a-zA-Z0-9\_\-\.]{1,20}$'
DOMAIN_REGEX = u'^[a-zA-Z0-9\_\-]{1,20}$'
PASSWORD_REGEX = u'^.{8,20}$'
USERNAME_REGEX = u'^[a-zA-Z0-9\_\-\.]{1,20}$'


def validate_name(name):

    return name and re.match(NAME_REGEX, name)


def validate_email(email):

    if email and '@' in email:
        fields = email.split('@')

        if len(fields) == 2:
            username = fields[0]
            domain = fields[1]

            if username and domain and re.match(USERNAME_REGEX, username):
                fields = domain.split('.')

                if len(fields) >= 2:

                    for field in fields:
                        if field and re.match(DOMAIN_REGEX, field):
                            return True
    return False


def validate_integer(value):
    try:
        int(value)
    except (ValueError, TypeError):
        return False

    return True


def validate_address(address):

    try:
        octets = address.split('.')
        if len(octets) != 4:
            return False
        for x in octets:
            if not (0 <= int(x) <= 255):
                return False
    except ValueError:
        return False
    return True


def validate_password(password):

    return password and re.match(PASSWORD_REGEX, password)


def validate_username(username):

    return username and re.match(NAME_REGEX, username)


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
    if address_list == u'':
        return {'status': False, 'desc': u'Server list can\'t be empty'}

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


def format_template_vars(template_vars):

    address_vars_group = dict()

    for oneline in template_vars.split('\n'):
        # 跳过template_vars中的空行
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