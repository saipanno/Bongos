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
from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, json, abort
from flask.ext.login import login_required, current_user

from frontend.extensions.database import db

from frontend.models.account import User, Group
from frontend.models.dashboard import SshConfig, PreDefinedScript, Server, Permission

from frontend.forms.account import CreateUserForm, EditUserForm, GroupForm
from frontend.forms.dashboard import PreDefinedScriptForm, SshConfigForm, ServerForm

from frontend.extensions.principal import UserAccessPermission
from frontend.extensions.utility import validate_name, validate_email, validate_username, \
    validate_password, validate_address


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/predefined_script/list')
@login_required
def list_predefined_script_ctrl():

    user_access = UserAccessPermission('dashboard.list_predefined_script_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    scripts = PreDefinedScript.query.all()

    for script in scripts:
        user = User.query.filter_by(id=int(script.author)).first()
        script.author_name = user.name

    return render_template('dashboard/predefined_script.html', scripts=scripts, type='list')


@dashboard.route('/predefined_script/<int:script_id>/show')
@login_required
def show_predefined_script_ctrl(script_id):

    user_access = UserAccessPermission('dashboard.show_predefined_script_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    default_next_page = request.values.get('next', url_for('account.index_ctrl'))

    try:
        script = PreDefinedScript.query.filter_by(id=script_id).first()

    except exc.SQLAlchemyError:
        flash(u'Internal database error', 'error')
        return redirect(default_next_page)
        # TODO: 增加异常日志记录

    if script is None:
        flash(u'PreDefined Script does not exist', 'error')
        return redirect(default_next_page)

    return render_template('dashboard/predefined_script.html', script=script, type='show')


@dashboard.route('/predefined_script/create', methods=("GET", "POST"))
@login_required
def create_predefined_script_ctrl():

    user_access = UserAccessPermission('dashboard.create_predefined_script_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = PreDefinedScriptForm()
    if request.method == 'GET':
        return render_template('dashboard/predefined_script.html', form=form, type='create')

    elif form.validate_on_submit():

        author = current_user.id

        script = PreDefinedScript(form.name.data, form.desc.data, form.script.data, author)
        db.session.add(script)
        db.session.commit()

        flash(u'Create predefined script successfully', 'success')
        return redirect(url_for('dashboard.list_predefined_script_ctrl'))

    else:
        return redirect(url_for('dashboard.create_predefined_script_ctrl'))


@dashboard.route('/predefined_script/<int:script_id>/edit', methods=("GET", "POST"))
@login_required
def edit_predefined_script_ctrl(script_id):

    user_access = UserAccessPermission('dashboard.edit_predefined_script_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    script = PreDefinedScript.query.filter_by(id=script_id).first()

    form = PreDefinedScriptForm(name=script.name, desc=script.desc, script=script.script)

    if request.method == 'GET':
        return render_template('dashboard/predefined_script.html', form=form, script=script, type='edit')

    elif form.validate_on_submit():

        if form.name.data != script.name:
            script.name = form.name.data

        if form.desc.data != script.desc:
            script.desc = form.desc.data

        if form.script.data != script.desc:
            script.script = form.script.data

        db.session.commit()

        flash(u'Update predefined script successfully.', 'success')
        return redirect(url_for('dashboard.list_predefined_script_ctrl'))

    else:
        return redirect(url_for('dashboard.edit_predefined_script_ctrl', script_id=script_id))


@dashboard.route('/user/list')
@login_required
def list_user_ctrl():

    user_access = UserAccessPermission('dashboard.list_user_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    users = User.query.all()

    for user in users:
        group = Group.query.filter_by(id=user.group).first()
        user.group_name = group.desc if group else u'None'

    return render_template('dashboard/user_manager.html', users=users, type='list')


@dashboard.route('/user/create', methods=("GET", "POST"))
@login_required
def create_user_ctrl():

    user_access = UserAccessPermission('dashboard.create_user_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = CreateUserForm()

    if form.validate_on_submit():

        user = User(form.email.data, form.username.data, form.name.data, form.group.data.id,
                    form.password.data, 1 if form.status.data else 0)
        db.session.add(user)
        db.session.commit()

        flash(u'Creating user successfully', 'success')

        return redirect(url_for('dashboard.list_user_ctrl'))

    else:
        return redirect(url_for('dashboard.create_user_ctrl'))


@dashboard.route('/user/<int:user_id>/edit', methods=("GET", "POST"))
@login_required
def edit_user_ctrl(user_id):

    user_access = UserAccessPermission('dashboard.edit_user_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    user = User.query.filter_by(id=user_id).first()

    form = EditUserForm(email=user.email, username=user.username, name=user.name, id=user.id)

    if request.method == 'GET':
        return render_template('dashboard/user_manager.html', form=form, type='edit')

    elif form.validate_on_submit():

        if form.name.data != user.name:
            user.name = form.name.data

        if form.group.data.id != user.group:
            user.group = form.group.data.id

        if len(form.new_password.data) > 0:
            user.update_password(form.new_password.data)

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

        return redirect(url_for('dashboard.list_user_ctrl'))

    else:
        return redirect(url_for('dashboard.edit_user_ctrl', user_id=user_id))


@dashboard.route('/user/<int:user_id>/update/<status>')
@login_required
def update_user_status_ctrl(user_id, status):

    user_access = UserAccessPermission('dashboard.update_user_status_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    user = User.query.filter_by(id=user_id).first()

    if status == '0':
        user.status = 0
        db.session.commit()

        flash(u'Disable user successfully', 'success')
    elif status == '1':
        user.status = 1
        db.session.commit()

        flash(u'Enable user successfully', 'success')
    elif status == 'delete':

        db.session.delete(user)
        db.session.commit()

        flash(u'Delete user successfully', 'success')

    else:
        flash(u'Incorrect user status format', 'error')

    return redirect(url_for('dashboard.list_user_ctrl'))


@dashboard.route('/ssh_config/list')
@login_required
def list_ssh_config_ctrl():

    user_access = UserAccessPermission('dashboard.list_ssh_config_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    ssh_configs = SshConfig.query.all()

    return render_template('dashboard/ssh_config.html', ssh_configs=ssh_configs, type='list')


@dashboard.route('/ssh_config/create', methods=("GET", "POST"))
@login_required
def create_ssh_config_ctrl():

    user_access = UserAccessPermission('dashboard.create_ssh_config_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = SshConfigForm()

    if request.method == 'GET':
        return render_template('dashboard/ssh_config.html', form=form, type='create')

    elif form.validate_on_submit():

        ssh_config = SshConfig(form.username.data, form.desc.data, form.port.data,
                               form.username.data, form.password.data, form.private_key.data)
        db.session.add(ssh_config)
        db.session.commit()

        flash(u'Creating ssh configuration successfully', 'success')

        return redirect(url_for('dashboard.list_ssh_config_ctrl'))

    else:
        return redirect(url_for('dashboard.create_ssh_config_ctrl'))


@dashboard.route('/ssh_config/<int:config_id>/edit', methods=("GET", "POST"))
@login_required
def edit_ssh_config_ctrl(config_id):

    user_access = UserAccessPermission('dashboard.edit_ssh_config_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    config = SshConfig.query.filter_by(id=config_id).first()

    form = SshConfigForm(name=config.name, desc=config.desc, port=config.port, username=config.username,
                         private_key=config.private_key)

    if request.method == 'GET':
        return render_template('dashboard/ssh_config.html', form=form, type='edit')

    elif form.validate_on_submit():

        if form.username.data != config.name:
            config.name = form.username.data

        if form.desc.data != config.desc:
            config.desc = form.desc.data

        if form.username.data != config.username:
            config.username = form.username.data

        if form.password.data != config.password:
            config.password = form.password.data

        if form.private_key.data != config.private_key:
            config.private_key = form.private_key.data

        db.session.commit()

        flash(u'Edit ssh configuration successfully', 'success')
        return redirect(url_for('dashboard.list_ssh_config_ctrl'))

    else:
        return redirect(url_for('dashboard.edit_ssh_config_ctrl', config_id=config_id))


@dashboard.route('/logging_reader')
@login_required
def logging_reader_ctrl():

    user_access = UserAccessPermission('dashboard.logging_reader_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    MAX_LEN = -200
    with open(current_app.config['LOGGING_FILENAME'], 'r') as f:
        logging_buffer = f.readlines()
        return render_template('dashboard/logging_reader.html', logging_buffer=logging_buffer[MAX_LEN:])


@dashboard.route('/group/list')
@login_required
def list_group_ctrl():

    user_access = UserAccessPermission('dashboard.list_group_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    groups = Group.query.all()
    for group in groups:

        group.members = ''
        try:
            users = User.query.filter_by(id=group.id).all()
        except Exception, e:
            users = None

        if users is not None:
            for user in users:
                group.members = '%s, %s' % (group.members, user.name)

    return render_template('dashboard/group_manager.html', groups=groups, type='list')


@dashboard.route('/group/create', methods=("GET", "POST"))
@login_required
def create_group_ctrl():

    user_access = UserAccessPermission('dashboard.create_group_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = GroupForm()

    if request.method == 'GET':

        return render_template('dashboard/group_manager.html', form=form, type='create')

    elif form.validate_on_submit():

        group = Group(form.name.data, form.desc.data)
        db.session.add(group)
        db.session.commit()

        flash(u'Create group successfully', 'success')
        return redirect(url_for('dashboard.list_group_ctrl'))

    else:
        return redirect(url_for('dashboard.create_group_ctrl'))


@dashboard.route('/group/<int:group_id>/edit', methods=("GET", "POST"))
@login_required
def edit_group_ctrl(group_id):

    user_access = UserAccessPermission('dashboard.edit_group_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    group = Group.query.filter_by(id=group_id).first()

    form = GroupForm(name=group.name, desc=group.desc, id=group.id)

    if request.method == 'GET':

        return render_template('dashboard/group_manager.html', form=form, type='edit')

    elif form.validate_on_submit():

        if form.name.data != group.name:
            group.name = form.name.data

        if form.desc.data != group.name:
            group.desc = form.desc.data

        db.session.commit()

        flash(u'Edit group successfully', 'success')
        return redirect(url_for('dashboard.list_group_ctrl'))

    else:
        return redirect(url_for('dashboard.edit_group_ctrl', group_id=group_id))


@dashboard.route('/server/list')
@login_required
def list_server_ctrl():

    user_access = UserAccessPermission('dashboard.list_server_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    servers = Server.query.all()

    for server in servers:

        try:
            group = Group.query.filter_by(id=server.group).first()
            server.group_name = group.name
        except Exception, e:
            server.group_name = u'None'

    return render_template('dashboard/server_manager.html', servers=servers, type='list')


@dashboard.route('/server/create', methods=("GET", "POST"))
@login_required
def create_server_ctrl():

    user_access = UserAccessPermission('dashboard.create_server_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = ServerForm()

    if request.method == 'GET':

        return render_template('dashboard/server_manager.html', form=form, type='create')

    elif form.validate_on_submit():

        server = Server(form.group.data.id, form.desc.data, form.ext_address.data, form.int_address.data,
                        form.ipmi_address.data, form.other_address.data, form.idc.data, form.rack.data,
                        form.manufacturer.data, form.model.data, form.cpu_info.data, form.disk_info.data,
                        form.memory_info.data)
        db.session.add(server)
        db.session.commit()

        flash(u'Create server successfully', 'success')
        return redirect(url_for('dashboard.list_server_ctrl'))

    else:
        return redirect(url_for('dashboard.create_server_ctrl'))


@dashboard.route('/server/<int:server_id>/edit', methods=("GET", "POST"))
@login_required
def edit_server_ctrl(server_id):

    user_access = UserAccessPermission('dashboard.edit_server_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    server = Server.query.filter_by(id=server_id).first()

    form = ServerForm(server)

    if request.method == 'GET':

        return render_template('dashboard/server_manager.html', form=form, type='edit')

    elif form.validate_on_submit():

        if form.group.data is not None:
            server.group = form.group.data.id

        if form.desc.data != server.desc:
            server.desc = form.desc.data

        if form.ext_address.data != server.ext_address:
            server.ext_address = form.ext_address.data

        if form.int_address.data != server.int_address:
            server.int_address = form.int_address.data

        if form.ipmi_address.data != server.ipmi_address:
            server.ipmi_address = form.ipmi_address.data

        if form.other_address.data != server.other_address:
            server.other_address = form.other_address.data

        if form.idc.data != server.idc:
            server.idc = form.idc.data

        if form.rack.data != server.rack:
            server.rack = form.rack.data

        if form.manufacturer.data != server.manufacturer:
            server.manufacturer = form.manufacturer.data

        if form.model.data != server.model:
            server.model = form.model.data

        if form.cpu_info.data != server.cpu_info:
            server.cpu_info = form.cpu_info.data

        if form.disk_info.data != server.disk_info:
            server.disk_info = form.disk_info.data

        if form.memory_info.data != server.memory_info:
            server.memory_info = form.memory_info.data

        server = Server(form.group.data.id, form.desc.data, form.ext_address.data, form.int_address.data,
                        form.ipmi_address.data, form.other_address.data, form.idc.data, form.rack.data,
                        form.manufacturer.data, form.model.data, form.cpu_info.data, form.disk_info.data,
                        form.memory_info.data)
        db.session.add(server)
        db.session.commit()

        flash(u'Edit server successfully', 'success')
        return redirect(url_for('dashboard.list_server_ctrl'))

    else:
        return redirect(url_for('dashboard.edit_server_ctrl', server_id=server_id))


@dashboard.route('/acl/list')
@login_required
def list_acl_ctrl():

    user_access = UserAccessPermission('dashboard.list_acl_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    groups = Group.query.all()

    group_information = dict()
    for group in groups:
        group_information[unicode(group.id)] = group.desc

    function_lists = list()
    access_control_dicts = dict()
    access_control_list = Permission.query.all()

    for access_control in access_control_list:

        function = access_control.function
        function_lists.append(function)

        try:
            access_rules = json.loads(access_control.access_rules)
        except Exception, e:
            access_rules = dict()

        for (group_id, status) in access_rules.items():

            try:
                access_control_dicts[group_id][function] = status
            except Exception:
                access_control_dicts[group_id] = dict()
                access_control_dicts[group_id][function] = status

    return render_template('dashboard/acl_manager.html', function_lists=function_lists, type='list',
                           group_information=group_information, access_control_dicts=access_control_dicts)


@dashboard.route('/acl/<function>/<group_id>/update/<int:status>')
@login_required
def update_acl_status_ctrl(function, group_id, status):

    user_access = UserAccessPermission('dashboard.update_acl_status_ctrl')
    if not user_access.can():
        flash('Do not have permissions, Forbidden', 'warning')
        return redirect(url_for('account.index_ctrl'))

    access_control = Permission.query.filter_by(function=function).first()

    try:
        access_rules = json.loads(access_control.access_rules)
    except Exception, e:
        access_rules = dict()

    if status == 0 or status == 1:
        access_rules[group_id] = status
    else:
        flash(u'Error ACL status', 'error')
        return redirect(url_for('dashboard.list_acl_ctrl'))

    access_control.access_rules = json.dumps(access_rules)
    db.session.commit()

    flash(u'Update ACL successfully', 'success')
    return redirect(url_for('dashboard.list_acl_ctrl'))
