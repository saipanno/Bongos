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


from sqlalchemy import desc
from flask import render_template, request, redirect, url_for, flash, session
from flask.ext.login import login_required, current_user

from web import db
from web import app

from web.models.dashboard import PreDefinedScript
from web.models.user import User
from web.models.operate import OperateDb

from web.forms.user import CreateUserForm

from web.forms.dashboard import CreatePreDefinedScriptForm


@app.route('/dashboard/script/list')
@login_required
def list_script_ctrl():

    if request.method == 'GET':

        scripts = PreDefinedScript.query.all()

        return render_template('dashboard/list_script.html', scripts=scripts)


@app.route('/dashboard/script/<int:script_id>/show')
@login_required
def show_script_ctrl(script_id):

    if request.method == 'GET':

        script = PreDefinedScript.query.filter_by(id=script_id).first()

        return render_template('dashboard/show_script.html', script=script)


@app.route('/dashboard/script/create', methods=("GET", "POST"))
@login_required
def create_script_ctrl():

    form = CreatePreDefinedScriptForm(name=u'', desc=u'', script=u'')

    if request.method == 'GET':

        return render_template('dashboard/edit_script.html', form=form, type='Create')

    elif request.method == 'POST':

        if form.desc.data == u'':

            flash(u'请输入脚本描述.', 'error')

        elif form.script.data == u'':

            flash(u'请输入脚本.', 'error')

        else:

            author = session['user'].username

            script = PreDefinedScript(form.name.data, form.desc.data, form.script.data, author)
            db.session.add(script)
            db.session.commit()

            flash(u'创建预定义脚本成功.', 'success')

        return redirect(url_for('list_script_ctrl'))


@app.route('/dashboard/script/<int:script_id>/edit', methods=("GET", "POST"))
@login_required
def edit_script_ctrl(script_id):

    script = PreDefinedScript.query.filter_by(id=script_id).first()

    form = CreatePreDefinedScriptForm(name=script.name, desc=script.desc, script=script.script)

    if request.method == 'GET':

        return render_template('dashboard/edit_script.html', type='Edit', form=form, script=script)

    elif request.method == 'POST':

        if form.desc.data == u'':

            flash(u'请输入脚本描述.', 'error')
            return redirect(url_for('list_script_ctrl'))

        elif form.script.data == u'':

            flash(u'请输入脚本.', 'error')
            return redirect(url_for('list_script_ctrl'))

        else:

            form.populate_obj(script)
            db.session.commit()

            flash(u'Edit script successful.', 'success')
            return redirect(url_for('list_script_ctrl'))


@app.route('/dashboard/user/list')
@login_required
def list_user_ctrl():

    if request.method == 'GET':

        users = User.query.all()

        return render_template('dashboard/list_user.html', users=users)


@app.route('/dashboard/user/<username>/show')
@login_required
def show_user_ctrl(username):

    if request.method == 'GET':

        user = User.query.filter_by(username=username).first()

        return render_template('dashboard/show_user.html', user=user)


@app.route('/dashboard/user/create', methods=("GET", "POST"))
@login_required
def create_user_ctrl():

    form = CreateUserForm(username=u'', nickname=u'', password=u'', group=u'')

    if request.method == 'GET':

        return render_template('dashboard/edit_user.html', form=form, type='Create')

    elif request.method == 'POST':

        if form.username.data == u'':

            flash(u'请输入用户名.', 'error')

        elif form.nickname.data == u'':

            flash(u'请输入昵称.', 'error')

        elif form.password.data == u'':

            flash(u'请输入密码.', 'error')

        else:

            user = User(form.username.data, form.nickname.data, form.password.data)
            db.session.add(current_user())
            db.session.commit()

            flash(u'创建用户成功.', 'success')

        return redirect(url_for('list_user_ctrl'))


@app.route('/dashboard/operate/list')
@login_required
def list_all_operate_ctrl():

    executes = OperateDb.query.order_by(desc(OperateDb.id)).all()

    return render_template('dashboard/list_operate.html', executes=executes)