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
from sqlalchemy import exc
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_required, current_user

from web import db

from web.user.models import User
from web.user.forms import CreateUserForm, EditUserForm

from web.dashboard.models import SshConfig, PreDefinedScript
from web.dashboard.forms import CreatePreDefinedScriptForm, CreateSshConfigForm

from web.extensions import validate_email, validate_username, validate_password


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/script/list')
@login_required
def list_script_ctrl():

    if request.method == 'GET':

        scripts = PreDefinedScript.query.all()

        return render_template('dashboard/predefined_script.html', scripts=scripts, type='list')


@dashboard.route('/script/<int:script_id>/show')
@login_required
def show_script_ctrl(script_id):

    default_next_page = request.values.get('next', url_for('user.index_ctrl'))

    try:
        script = PreDefinedScript.query.filter_by(id=script_id).first()

    except exc.SQLAlchemyError:
        flash(u'获取预定义脚本信息错误.', 'error')
        return redirect(default_next_page)

    if script is None:
        flash(u'不存在的预定义脚本.', 'error')
        return redirect(default_next_page)

    return render_template('dashboard/predefined_script.html', script=script, type='show')


@dashboard.route('/script/create', methods=("GET", "POST"))
@login_required
def create_script_ctrl():

    form = CreatePreDefinedScriptForm()

    if request.method == 'GET':

        return render_template('dashboard/predefined_script.html', form=form, type='create')

    elif request.method == 'POST':

        if form.desc.data == u'':

            flash(u'请输入脚本描述.', 'error')

        elif form.script.data == u'':

            flash(u'请输入脚本.', 'error')

        else:

            author = current_user.name

            script = PreDefinedScript(form.name.data, form.desc.data, form.script.data, author)
            db.session.add(script)
            db.session.commit()

            flash(u'创建预定义脚本成功.', 'success')

        return redirect(url_for('dashboard.list_script_ctrl'))


@dashboard.route('/script/<int:script_id>/edit', methods=("GET", "POST"))
@login_required
def edit_script_ctrl(script_id):

    script = PreDefinedScript.query.filter_by(id=script_id).first()

    form = CreatePreDefinedScriptForm(name=script.name, desc=script.desc, script=script.script)

    if request.method == 'GET':

        return render_template('dashboard/predefined_script.html', form=form, script=script, type='edit')

    elif request.method == 'POST':

        if form.desc.data == u'':

            flash(u'请输入脚本描述.', 'error')
            return redirect(url_for('dashboard.list_script_ctrl'))

        elif form.script.data == u'':

            flash(u'请输入脚本.', 'error')
            return redirect(url_for('dashboard.list_script_ctrl'))

        else:

            form.populate_obj(script)
            db.session.commit()

            flash(u'Edit script successful.', 'success')
            return redirect(url_for('dashboard.list_script_ctrl'))


@dashboard.route('/user/list')
@login_required
def list_user_ctrl():

    if request.method == 'GET':

        users = User.query.all()

        return render_template('dashboard/user.html', users=users, type='list')


@dashboard.route('/user/create', methods=("GET", "POST"))
@login_required
def create_user_ctrl():

    form = CreateUserForm()

    if request.method == 'GET':

        return render_template('dashboard/user.html', form=form, type='create')

    elif request.method == 'POST':

        if not validate_email(form.email.data):
            flash(u'不符合要求的邮箱地址.', 'error')

        elif not validate_username(form.name.data):
            flash(u'不符合要求的用户名.', 'error')

        elif form.password.data != form.confirm_password.data:
            flash(u'请输入相同的密码.', 'error')

        elif not validate_password(form.password.data):
            flash(u'不符合要求的密码.', 'error')

        else:
            user = User(form.email.data, form.name.data, form.password.data)
            db.session.add(user)
            db.session.commit()

            flash(u'创建用户成功.', 'success')

        return redirect(url_for('dashboard.list_user_ctrl'))


@dashboard.route('/user/<int:user_id>/edit', methods=("GET", "POST"))
@login_required
def edit_user_ctrl(user_id):

    user = User.query.filter_by(id=user_id).first()

    form = EditUserForm(email=user.email, name=user.name)

    if request.method == 'GET':

        return render_template('dashboard/user.html', form=form, type='edit')

    elif request.method == 'POST':

        if not validate_email(form.email.data):
            flash(u'不符合要求的邮箱地址.', 'error')

        elif not validate_username(form.name.data):
            flash(u'不符合要求的用户名.', 'error')

        elif form.new_password.data != form.confirm_password.data:
            flash(u'两次密码不一致.', 'error')

        elif len(form.new_password.data) > 0:

            if user.check_password(form.now_password.data):

                if validate_password(form.new_password.data):
                    user.update_password(form.new_password.data)

                    form.populate_obj(user)
                    db.session.commit()

                    flash(u'编辑用户成功.', 'success')
                else:
                    flash(u'密码不符合要求.', 'error')
            else:
                flash(u'当前密码错误.', 'error')

        else:

            form.populate_obj(user)
            db.session.commit()

            flash(u'编辑用户成功.', 'success')

        return redirect(url_for('dashboard.list_user_ctrl'))


@dashboard.route('/ssh_config/list')
@login_required
def list_ssh_config_ctrl():

    if request.method == 'GET':

        ssh_configs = SshConfig.query.all()

        return render_template('dashboard/ssh_config.html', ssh_configs=ssh_configs, type='list')


@dashboard.route('/ssh_config/create', methods=("GET", "POST"))
@login_required
def create_ssh_config_ctrl():

    form = CreateSshConfigForm()

    if request.method == 'GET':

        return render_template('dashboard/ssh_config.html', form=form, type='create')

    elif request.method == 'POST':

        redirect_url = url_for('dashboard.create_ssh_config_ctrl')

        if form.name.data != u'':
            flash(u'Name can\'t be empty', 'error')
        elif SshConfig.query.filter_by(name=form.name.data).all():
            flash(u'The current name is already in use', 'error')

        elif form.desc.data != u'':
            flash(u'Description can\'t be empty', 'error')

        elif form.port.data != u'':
            flash(u'Port can\'t be empty', 'error')
        elif form.port.data is None:
            flash(u'Port can only be an integer', 'error')

        elif form.username.data != u'':
            flash(u'Username can\'t be empty', 'error')
        elif not re.match("^[a-z0-9]{1,20}$", form.username.data):
            flash(u'Wrong username format', 'error')

        elif form.password.data != u'':
            flash(u'Password can\'t be empty', 'error')

        elif not re.match("^[a-z0-9\-\.]{1,20}$", form.private_key.data):
            flash(u'Wrong key filename', 'error')

        else:

            ssh_config = SshConfig(form.name.data, form.desc.data, form.port.data,
                                   form.username.data, form.password.data, form.private_key.data)
            db.session.add(ssh_config)
            db.session.commit()

            flash(u'Create ssh configuration successfully', 'success')
            redirect_url = url_for('dashboard.list_ssh_config_ctrl')

        return redirect(redirect_url)


@dashboard.route('/ssh_config/<int:config_id>/edit', methods=("GET", "POST"))
@login_required
def edit_ssh_config_ctrl(config_id):

    config = SshConfig.query.filter_by(id=config_id).first()

    form = CreateSshConfigForm(name=config.name, desc=config.desc, port=config.port, username=config.username,
                               private_key=config.private_key)

    if request.method == 'GET':

        return render_template('dashboard/ssh_config.html', form=form, type='edit')

    elif request.method == 'POST':

        if form.name.data != config.name and form.name.data != u'':
            if SshConfig.query.filter_by(name=form.name.data).all():
                flash(u'The current name is already in use', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))
            else:
                config.name = form.name.data

        if form.desc.data != config.desc and form.desc.data != u'':
            config.desc = form.desc.data

        try:
            if form.port.data != config.port and form.port.data != u'':
                config.port = int(form.port.data)
        except TypeError:
            flash(u'Port can only be an integer', 'error')
            return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))

        if form.username.data != config.username and form.username.data != u'':
            if re.match("^[a-z0-9]{1,20}$", form.username.data):
                config.username = form.username.data
            else:
                flash(u'Wrong username format', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))

        if form.password.data != config.password and form.password.data != u'':
                config.password = form.password.data

        if form.private_key.data != config.private_key and form.private_key.data != u'':
            if re.match("^[a-z0-9\-\.]{1,20}$", form.private_key.data):
                config.private_key = form.private_key.data
            else:
                flash(u'Wrong key filename', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))

        db.session.commit()

        flash(u'Update ssh configuration successfully', 'success')
        return redirect(url_for('dashboard.list_ssh_config_ctrl'))