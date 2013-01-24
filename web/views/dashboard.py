#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/23.
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
from flask import render_template, request, redirect, url_for, flash, session

from web import db
from web import app

from web.models.dashboard import PreDefinedScript

from web.forms.dashboard import PreDefinedScriptCreate

from web.extensions import login_required

@app.route('/dashboard')
@login_required
def index_dashboard_ctrl():

    if request.method == 'GET':

        return render_template('dashboard/show_predefined_script.html')


@app.route('/dashboard/show/predefined')
@login_required
def show_predefined_ctrl():

    if request.method == 'GET':

        regex = '^[0-9]+$'
        operate_id = request.args.get('id', None)

        #if operate_id is not None and re.match(regex, operate_id) is not None:

        #    script = PreDefinedScript.query.filter_by(id=operate_id).first()

        #    return render_template('dashboard/create_predefined_script.html', type='show', script=script)

        #else:

        scripts = PreDefinedScript.query.all()

        return render_template('dashboard/show_predefined_script.html', scripts=scripts)

@app.route('/dashboard/create/default', methods=("GET", "POST"))
@login_required
def create_predefined_ctrl():

    form = PreDefinedScriptCreate()

    if request.method == 'GET':

        return render_template('dashboard/create_predefined_script.html', form=form)

    elif request.method == 'POST':

        if form.desc.data == u'None' or form.script.data == u'None':
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_predefined_operate_ctrl'))
        else:

            author = session['user'].username

            script = PreDefinedScript(form.name.data, form.desc.data, form.script.data, author)
            db.session.add(script)
            db.session.commit()

            flash(u'Create script successful.', 'success')
            return redirect(url_for('show_predefined_ctrl'))
