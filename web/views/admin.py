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


from flask import render_template, request, redirect, url_for, flash, session

from web import db
from web import app

from web.models.admin import PreDefinedScript
from web.models.user import User

from web.forms.user import CreateUserForm

from web.forms.admin import CreatePreDefinedScriptForm

from web.extensions import login_required

@app.route('/admin')
@login_required
def index_dashboard_ctrl():

    if request.method == 'GET':

        return render_template('admin/show_script.html')


@app.route('/admin/script/list')
@login_required
def list_script_ctrl():

    if request.method == 'GET':

        scripts = PreDefinedScript.query.all()

        return render_template('admin/show_script.html', scripts=scripts, type='List')


@app.route('/admin/script/show/<int:script_id>')
@login_required
def show_script_ctrl(script_id):

    if request.method == 'GET':

        script = PreDefinedScript.query.filter_by(id=script_id).first()

        return render_template('admin/show_script.html', script=script, type='Show')


@app.route('/admin/script/create', methods=("GET", "POST"))
@login_required
def create_script_ctrl():

    form = CreatePreDefinedScriptForm(name=u'', desc=u'', script=u'')

    if request.method == 'GET':

        return render_template('admin/submit_script.html', form=form, type='Create')

    elif request.method == 'POST':

        if form.desc.data == u'' or form.script.data == u'':

            flash(u'Some input is None.', 'error')

        else:

            author = session['user'].username

            script = PreDefinedScript(form.name.data, form.desc.data, form.script.data, author)
            db.session.add(script)
            db.session.commit()

            flash(u'Create script successful.', 'success')

        return redirect(url_for('show_script_ctrl'))


@app.route('/admin/script/edit/<int:script_id>', methods=("GET", "POST"))
@login_required
def edit_script_ctrl(script_id):

    script = PreDefinedScript.query.filter_by(id=script_id).first()

    form = CreatePreDefinedScriptForm(name=script.name, desc=script.desc, script=script.script)

    if request.method == 'GET':

        return render_template('admin/submit_script.html', type='Edit', form=form, script=script)

    elif request.method == 'POST':

        if form.desc.data == u'' or form.script.data == u'':

            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_script_ctrl'))
        else:

            form.populate_obj(script)
            db.session.commit()

            flash(u'Edit script successful.', 'success')
            return redirect(url_for('list_script_ctrl'))


@app.route('/admin/user/list')
@login_required
def list_user_ctrl():

    if request.method == 'GET':

        users = User.query.all()

        return render_template('admin/show_user.html', users=users, type='List')


@app.route('/admin/user/show/<int:user_id>')
@login_required
def show_user_ctrl(user_id):

    if request.method == 'GET':

        user = User.query.filter_by(id=user_id).first()

        return render_template('admin/show_user.html', user=user, type='Show')


@app.route('/admin/user/create', methods=("GET", "POST"))
@login_required
def create_user_ctrl():

    form = CreateUserForm(username=u'', nickname=u'', password=u'', group=u'')

    if request.method == 'GET':

        return render_template('admin/submit_user.html', form=form, type='Create')

    elif request.method == 'POST':

        if form.username.data == u'' or form.nickname.data == u'' or form.password.data == u'':

            flash(u'Some input is None.', 'error')

        else:

            user = User(form.username.data, form.nickname.data, form.password.data)
            db.session.add(user)
            db.session.commit()

            flash(u'Create user successful.', 'success')

        return redirect(url_for('show_user_ctrl'))