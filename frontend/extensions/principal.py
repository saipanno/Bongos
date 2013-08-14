#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/07/11.
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


import functools
from flask import flash, url_for, redirect

from flask.ext.principal import Need, Permission


AuthorizeNeed = functools.partial(Need, 'handler')


class AuthorizePermission(Permission):

    def __init__(self, name):
        need = AuthorizeNeed(name)
        super(AuthorizePermission, self).__init__(need)


class AuthorizeRequired(object):
    bp = ''

    def __init__(self, bp=None):
        self.bp = bp if bp else ''

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            access = AuthorizePermission('%s.%s' % (self.bp, f.__name__))
            if not access.can():
                flash(u'Don\'t have permission to access this link', 'error')
                return redirect(url_for('account.index_ctrl'))

            return f(*args, **kwargs)

        return wrapper