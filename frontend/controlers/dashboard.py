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


from sqlalchemy import exc
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_required, current_user

from frontend.extensions.database import db

from frontend.models.member import User, PermissionGroup
from frontend.models.dashboard import SshConfig, PreDefinedScript

from frontend.forms.member import CreateUserForm, EditUserForm
from frontend.forms.dashboard import CreatePreDefinedScriptForm, CreateSshConfigForm

from frontend.extensions.utility import validate_name, validate_email, validate_username, validate_password
from frontend.extensions.principal import admin_permission, member_permission

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/predefined_script/list')
@login_required
def list_predefined_script_ctrl():

    if request.method == 'GET':

        scripts = PreDefinedScript.query.all()

        for script in scripts:
            user = User.query.filter_by(id=int(script.author)).first()
            script.author = user.username

        return render_template('dashboard/predefined_script.html', scripts=scripts, type='list')


@dashboard.route('/predefined_script/<int:script_id>/show')
@login_required
def show_predefined_script_ctrl(script_id):

    default_next_page = request.values.get('next', url_for('member.index_ctrl'))

    try:
        script = PreDefinedScript.query.filter_by(id=script_id).first()

    except exc.SQLAlchemyError:
        flash(u'Internal database error', 'error')
        return redirect(default_next_page)

    if script is None:
        flash(u'This predefined script does not exist', 'error')
        return redirect(default_next_page)

    return render_template('dashboard/predefined_script.html', script=script, type='show')


@dashboard.route('/predefined_script/create', methods=("GET", "POST"))
@login_required
def create_predefined_script_ctrl():

    form = CreatePreDefinedScriptForm()

    if request.method == 'GET':

        return render_template('dashboard/predefined_script.html', form=form, type='create')

    elif request.method == 'POST':

        author = current_user.id
        redirect_url = url_for('dashboard.create_predefined_script_ctrl')

        if form.username.data == u'':
            flash(u'Name can\'t be empty', 'error')
        elif not validate_name(form.username.data):
            flash(u'Incorrect name format', 'error')
        elif PreDefinedScript.query.filter_by(name=form.username.data).all():
            flash(u'The current name is already in use', 'error')

        elif form.desc.data == u'':
            flash(u'Script description can\'t be empty', 'error')

        elif form.script.data == u'':
            flash(u'Script can\'t be empty', 'error')

        else:

            script = PreDefinedScript(form.username.data, form.desc.data, form.script.data, author)
            db.session.add(script)
            db.session.commit()

            flash(u'Create predefined script successfully', 'success')

        return redirect(redirect_url)


@dashboard.route('/predefined_script/<int:script_id>/edit', methods=("GET", "POST"))
@login_required
def edit_predefined_script_ctrl(script_id):

    script = PreDefinedScript.query.filter_by(id=script_id).first()

    form = CreatePreDefinedScriptForm(name=script.name, desc=script.desc, script=script.script)

    if request.method == 'GET':

        return render_template('dashboard/predefined_script.html', form=form, script=script, type='edit')

    elif request.method == 'POST':

        if form.username.data != script.name and form.username.data != u'':
            if not validate_name(form.username.data):
                flash(u'Incorrect name format', 'error')
                return redirect(url_for('dashboard.edit_predefined_script_ctrl', script_id=script_id))

        if form.desc.data != script.desc and form.desc.data != u'':
            script.desc = form.desc.data

        if form.script.data != script.desc and form.script.data != u'':
            script.script = form.script.data

        db.session.commit()

        flash(u'Update predefined script successfully.', 'success')
        return redirect(url_for('dashboard.list_predefined_script_ctrl'))


@dashboard.route('/user/list')
@login_required
def list_user_ctrl():

    if request.method == 'GET':

        users = User.query.all()

        for user in users:
            user.group = PermissionGroup.query.filter_by(id=user.group).first().desc

        return render_template('dashboard/user_manager.html', users=users, type='list')


@dashboard.route('/user/create', methods=("GET", "POST"))
@login_required
def create_user_ctrl():

    form = CreateUserForm()

    if request.method == 'GET':

        return render_template('dashboard/user_manager.html', form=form, type='create')

    elif request.method == 'POST':

        redirect_url = url_for('dashboard.create_user_ctrl')

        if form.email.data == u'':
            flash(u'Email can\'t be empty', 'error')
        elif User.query.filter_by(email=form.email.data).all():
            flash(u'The current email is already in use', 'error')
        elif not validate_email(form.email.data):
            flash(u'Incorrect e-mail address', 'error')

        elif form.username.data == u'':
            flash(u'Name can\'t be empty', 'error')
        elif User.query.filter_by(username=form.username.data).all():
            flash(u'The current name is already in use', 'error')
        elif not validate_name(form.username.data):
            flash(u'Incorrect name format', 'error')

        elif form.group.data.id is None:
            flash(u'Group can\'t be empty', 'error')
        elif not PermissionGroup.query.filter_by(id=form.group.data.id).all():
            flash(u'The current group is not exist', 'error')

        elif form.password.data == u'' or form.confirm_password.data == u'':
            flash(u'Password can\'t be empty', 'error')
        elif form.password.data != form.confirm_password.data:
            flash(u'Please enter the same password', 'error')
        elif not validate_password(form.password.data):
            flash(u'Incorrect password format', 'error')

        else:
            user = User(form.email.data, form.username.data, form.group.data.id, form.password.data, form.status.data)
            db.session.add(user)
            db.session.commit()

            flash(u'Create user successfully', 'success')
            redirect_url = url_for('dashboard.list_user_ctrl')

        return redirect(redirect_url)


@dashboard.route('/user/<int:user_id>/edit', methods=("GET", "POST"))
@login_required
def edit_user_ctrl(user_id):

    user = User.query.filter_by(id=user_id).first()

    form = EditUserForm(email=user.email, username=user.username, group=user.group)

    if request.method == 'GET':

        return render_template('dashboard/user_manager.html', form=form, type='edit')

    elif request.method == 'POST':

        if form.email.data != user.email and form.email.data != u'':
            if User.query.filter_by(email=form.email.data).all():
                flash(u'The current email is already in use', 'error')
                return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))
            elif not validate_email(form.email.data):
                flash(u'Incorrect e-mail address', 'error')
                return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))
            else:
                user.email = form.email.data

        if form.username.data != user.username and form.username.data != u'':
            if User.query.filter_by(username=form.username.data).all():
                flash(u'The current name is already in use', 'error')
                return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))
            elif not validate_name(form.username.data):
                flash(u'Incorrect name format', 'error')
                return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))
            else:
                user.username = form.username.data

        if form.group.data.id != user.group and form.group.data.id is not None:
            if not PermissionGroup.query.filter_by(id=form.group.data.id).all():
                flash(u'The current group is not exist', 'error')
            else:
                user.group = form.group.data.id

        if len(form.new_password.data) > 0:

            if form.new_password.data != form.confirm_password.data:
                flash(u'Please enter the same password', 'error')
                return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))
            elif not validate_password(form.new_password.data):
                flash(u'Incorrect password format', 'error')
                return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))
            else:
                user.update_password(form.new_password.data)

        if form.status.data != user.status:
            user.status = form.status.data

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

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

        if form.username.data == u'':
            flash(u'Name can\'t be empty', 'error')
        elif not validate_name(form.username.data):
            flash(u'Incorrect name format', 'error')
        elif SshConfig.query.filter_by(name=form.username.data).all():
            flash(u'The current name is already in use', 'error')

        elif form.desc.data == u'':
            flash(u'Description can\'t be empty', 'error')

        elif form.port.data == u'':
            flash(u'Port can\'t be empty', 'error')
        elif form.port.data is None:
            flash(u'Port can only be an integer', 'error')

        elif form.username.data == u'':
            flash(u'Username can\'t be empty', 'error')
        elif not validate_username(form.username.data):
            flash(u'Incorrect username format', 'error')

        elif form.password.data == u'':
            flash(u'Password can\'t be empty', 'error')

        elif form.private_key.data != u'' and not validate_name(form.private_key.data):
            flash(u'Incorrect key filename format', 'error')

        else:

            ssh_config = SshConfig(form.username.data, form.desc.data, form.port.data,
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

        if form.username.data != config.name and form.username.data != u'':
            if SshConfig.query.filter_by(name=form.username.data).all():
                flash(u'The current name is already in use', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))
            elif not validate_name(form.username.data):
                flash(u'Incorrect name format', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', script_id=config_id))
            else:
                config.name = form.username.data

        if form.desc.data != config.desc and form.desc.data != u'':
            config.desc = form.desc.data

        try:
            if form.port.data != config.port and form.port.data != u'':
                config.port = int(form.port.data)
        except TypeError:
            flash(u'Port can only be an integer', 'error')
            return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))

        if form.username.data != config.username and form.username.data != u'':
            if validate_username(form.username.data):
                config.username = form.username.data
            else:
                flash(u'Incorrect username format', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))

        if form.password.data != config.password and form.password.data != u'':
                config.password = form.password.data

        if form.private_key.data != config.private_key and form.private_key.data != u'':
            if validate_name(form.private_key.data):
                config.private_key = form.private_key.data
            else:
                flash(u'Incorrect key filename format', 'error')
                return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))

        db.session.commit()

        flash(u'Update ssh configuration successfully', 'success')
        return redirect(url_for('dashboard.list_ssh_config_ctrl'))