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


from flask import Flask, render_template, json
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, Principal

from frontend.models.dashboard import AccessControl

from frontend.extensions.database import db
from frontend.extensions.login_manager import login
from frontend.extensions.principal import UserAccessNeed


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object('settings')
    if config is not None:
        app.config.from_object(config)

    configure_extensions(app)
    configure_blueprints(app)

    return app


def configure_extensions(app):

    # config Flask-SQLAlchemy
    db.app = app
    db.init_app(app)

    # config Flask-Login
    login.init_app(app)

    # config Flask-Principal
    principal = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):

        if hasattr(current_user, 'group'):
            access_control_list = AccessControl.query.all()
            for access_control in access_control_list:

                groups_access = json.loads(access_control.groups_access)
                for group_id in groups_access:

                    if current_user.group == group_id and groups_access[group_id] == 1:
                        identity.provides.add(UserAccessNeed(access_control.function))


def configure_blueprints(app):

    import frontend.controlers

    BLUEPRINTS = (
        frontend.controlers.account,
        frontend.controlers.operation,
        frontend.controlers.dashboard
    )

    for blueprint in BLUEPRINTS:

        app.register_blueprint(blueprint)