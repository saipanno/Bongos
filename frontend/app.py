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


from flask import Flask

from frontend.extensions.database import db
from frontend.extensions.login_manager import login
from frontend.extensions.principal import principal


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
    principal.init_app(app)


def configure_blueprints(app):

    import frontend.controlers

    BLUEPRINTS = (
        frontend.controlers.member,
        frontend.controlers.operation,
        frontend.controlers.dashboard
    )

    for blueprint in BLUEPRINTS:

        app.register_blueprint(blueprint)