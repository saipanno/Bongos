#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/21.
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

from web import login_manager

from web.user.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def verify_address(address):
    """
    Returns True if `address` is a valid IPv4 address.

    >>> verify_address('192.168.1.1')
    True
    >>> verify_address('192.168.1.800')
    False
    >>> verify_address('192.168.1')
    False
    """
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
        return {'status': False, 'desc': u'空白服务器列表.'}

    try:
        new_address_list = str()
        for server in re.split(';|,| |\n', address_list):
            if server == u'':
                continue
            address_status = verify_address(server.strip())
            if address_status is not True:
                return {'status': False, 'desc': u'错误的服务器地址: %s' % server}
            new_address_list = '%s %s' % (new_address_list, server.strip())
    except Exception, e:
        return {'status': False, 'desc': u'%s' % e}

    return {'status': True, 'desc': u'%s' % new_address_list.strip()}


def format_template_vars(template_vars):

    address_vars_group = dict()

    for oneline in template_vars.split('\n'):
        # 跳过template_vars中的空行
        if oneline == u'':
            continue
        try:
            address = oneline.split('|')[0]
            if address == u'':
                return {'status': False, 'desc': u'错误的变量赋值，不存在address关键字.'}
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
                    return {'status': False, 'desc': u'错误的变量赋值: %s' % var}
        except IndexError:
            return {'status': False, 'desc': u'错误的变量赋值: %s' % oneline}

    return {'status': True, 'desc': address_vars_group}


def validate_email(email):
    EMAIL_RE = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

    user = User.query.filter_by(email=email).all()

    if user:
        return False
    else:
        return email and EMAIL_RE.match(email)


def validate_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

    user = User.query.filter_by(name=username).all()

    if user:
        return False
    else:
        return username and USER_RE.match(username)


def validate_password(password):
    PASSWORD_RE = re.compile(r".{8,20}$")

    return password and PASSWORD_RE.match(password)