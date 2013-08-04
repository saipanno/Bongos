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
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import io
from flask import current_app
from flask.ext.script import prompt_bool, Manager

from frontend.app import create_app


app = create_app()
manager = Manager(app)


@manager.command
def init_db():
    """Create Default Database."""
    from frontend.extensions.database import db

    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Drop Current Database."""
    from frontend.extensions.database import db

    if prompt_bool(u'Are you sure you want to lose all your data:'):
        db.drop_all()


@manager.command
def init_ugp():
    """Create Default User, Group and Permissions."""
    from frontend.models.account import User, Group
    from frontend.models.dashboard import Permission
    from frontend.extensions.database import db

    user = User(email='admin@bongos', username='admin', name='Administrator', groups='1', password='admin', status=1)
    group = Group(name='Administrator', desc='Super Administrator Group')
    db.session.add(user)
    db.session.add(group)

    with io.open(current_app.config.get('BASIC_PERMISSION_LIST'), 'rt') as f:
        for oneline in f.readlines():
            function, desc = oneline.split(',')
            permission = Permission(desc=desc, function=function, rules=u'1')
            db.session.add(permission)

    db.session.commit()


if __name__ == '__main__':

    manager.run()