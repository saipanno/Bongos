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

from frontend.models.member import User, Group
from frontend.models.dashboard import SshConfig, PreDefinedScript, Server, AccessControl

from frontend.forms.member import CreateUserForm, EditUserForm
from frontend.forms.dashboard import CreatePreDefinedScriptForm, CreateSshConfigForm, ServerForm, AccessControlForm

from frontend.extensions.principal import UserAccessPermission
from frontend.extensions.utility import validate_name, validate_email, validate_username, \
    validate_password, validate_address


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/predefined_script/list')
@login_required
def list_predefined_script_ctrl():

    user_access = UserAccessPermission('dashboard.list_predefined_script_ctrl')
    if not user_access.can():
        abort(403)

    if request.method == 'GET':

        scripts = PreDefinedScript.query.all()

        for script in scripts:
            user = User.query.filter_by(id=int(script.author)).first()
            script.author_name = user.username

        return render_template('dashboard/predefined_script.html', scripts=scripts, type='list')


@dashboard.route('/predefined_script/<int:script_id>/show')
@login_required
def show_predefined_script_ctrl(script_id):

    user_access = UserAccessPermission('dashboard.show_predefined_script_ctrl')
    if not user_access.can():
        abort(403)

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

    user_access = UserAccessPermission('dashboard.create_predefined_script_ctrl')
    if not user_access.can():
        abort(403)

    form = CreatePreDefinedScriptForm()

    if request.method == 'GET':

        return render_template('dashboard/predefined_script.html', form=form, type='create')

    elif request.method == 'POST':

        author = current_user.id
        redirect_url = url_for('dashboard.create_predefined_script_ctrl')

        if form.name.data == u'':
            flash(u'Name can\'t be empty', 'error')
        elif not validate_name(form.name.data):
            flash(u'Incorrect name format', 'error')
        elif PreDefinedScript.query.filter_by(name=form.name.data).all():
            flash(u'The current name is already in use', 'error')

        elif form.desc.data == u'':
            flash(u'Script description can\'t be empty', 'error')

        elif form.script.data == u'':
            flash(u'Script can\'t be empty', 'error')

        else:

            script = PreDefinedScript(form.name.data, form.desc.data, form.script.data, author)
            db.session.add(script)
            db.session.commit()

            flash(u'Create predefined script successfully', 'success')

        return redirect(redirect_url)



@dashboard.route('/predefined_script/<int:script_id>/edit', methods=("GET", "POST"))
@login_required
def edit_predefined_script_ctrl(script_id):

    user_access = UserAccessPermission('dashboard.edit_predefined_script_ctrl')
    if not user_access.can():
        abort(403)

    script = PreDefinedScript.query.filter_by(id=script_id).first()

    form = CreatePreDefinedScriptForm(name=script.name, desc=script.desc, script=script.script)

    if request.method == 'GET':

        return render_template('dashboard/predefined_script.html', form=form, script=script, type='edit')

    elif request.method == 'POST':

        if form.name.data != script.name and form.name.data != u'':
            if not validate_name(form.name.data):
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

    user_access = UserAccessPermission('dashboard.list_user_ctrl')
    if not user_access.can():
        abort(403)

    if request.method == 'GET':

        users = User.query.all()

        for user in users:
            user.group_name = Group.query.filter_by(id=user.group).first().desc

        return render_template('dashboard/user_manager.html', users=users, type='list')


@dashboard.route('/user/create', methods=("GET", "POST"))
@login_required
def create_user_ctrl():

    user_access = UserAccessPermission('dashboard.create_user_ctrl')
    if not user_access.can():
        abort(403)

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
        elif not Group.query.filter_by(id=form.group.data.id).all():
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

    user_access = UserAccessPermission('dashboard.edit_user_ctrl')
    if not user_access.can():
        abort(403)

    user = User.query.filter_by(id=user_id).first()

    form = EditUserForm(email=user.email, username=user.username)

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
            if not Group.query.filter_by(id=form.group.data.id).all():
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

    user_access = UserAccessPermission('dashboard.list_ssh_config_ctrl')
    if not user_access.can():
        abort(403)

    if request.method == 'GET':

        ssh_configs = SshConfig.query.all()

        return render_template('dashboard/ssh_config.html', ssh_configs=ssh_configs, type='list')


@dashboard.route('/ssh_config/create', methods=("GET", "POST"))
@login_required
def create_ssh_config_ctrl():

    user_access = UserAccessPermission('dashboard.create_ssh_config_ctrl')
    if not user_access.can():
        abort(403)

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

    user_access = UserAccessPermission('dashboard.edit_ssh_config_ctrl')
    if not user_access.can():
        abort(403)

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


@dashboard.route('/logging_reader')
@login_required
def logging_reader_ctrl():

    user_access = UserAccessPermission('dashboard.logging_reader_ctrl')
    if not user_access.can():
        abort(403)

    MAX_LEN = -200
    with open(current_app.config['LOGGING_FILENAME'], 'r') as f:
        logging_buffer = f.readlines()
        return render_template('dashboard/logging_reader.html', logging_buffer=logging_buffer[MAX_LEN:])


@dashboard.route('/group/list')
@login_required
def list_group_ctrl():

    user_access = UserAccessPermission('dashboard.list_group_ctrl')
    if not user_access.can():
        abort(403)

    if request.method == 'GET':

        groups = Group.query.all()
        for group in groups:

            group.members = ''
            try:
                users = User.query.filter_by(id=group.id).all()
            except Exception, e:
                users = None
            finally:
                if users is not None:
                    for user in users:
                        group.members = '%s, %s' % (group.members, user.username)

        return render_template('dashboard/group_manager.html', groups=groups, type='list')


@dashboard.route('/server/list')
@login_required
def list_server_ctrl():

    user_access = UserAccessPermission('dashboard.list_server_ctrl')
    if not user_access.can():
        abort(403)

    if request.method == 'GET':

        servers = Server.query.all()

        for server in servers:

            try:
                server.group_name = Group.query.filter_by(id=server.group).first()
            except Exception, e:
                server.group_name = u'None'

        return render_template('dashboard/server_manager.html', servers=servers, type='list')


@dashboard.route('/server/create', methods=("GET", "POST"))
@login_required
def create_server_ctrl():

    user_access = UserAccessPermission('dashboard.create_server_ctrl')
    if not user_access.can():
        abort(403)

    form = ServerForm()

    if request.method == 'GET':

        return render_template('dashboard/server_manager.html', form=form, type='create')

    elif request.method == 'POST':

        redirect_url = url_for('dashboard.create_server_ctrl')

        if form.group.data.id is None:
            flash(u'Group can\'t be empty', 'error')
        elif not Group.query.filter_by(id=form.group.data.id).all():
            flash(u'The current group is not exist', 'error')

        elif form.ext_address.data != u'' and Server.query.filter_by(ext_address=form.ext_address.data).all():
            flash(u'The current ext_address is already in use', 'error')
        elif form.ext_address.data != u'' and not validate_address(form.ext_address.data):
            flash(u'Incorrect ext_address', 'error')

        elif form.int_address.data != u'' and Server.query.filter_by(int_address=form.int_address.data).all():
            flash(u'The current int_address is already in use', 'error')
        elif form.int_address.data != u'' and not validate_address(form.int_address.data):
            flash(u'Incorrect int_address', 'error')

        elif form.ipmi_address.data != u'' and Server.query.filter_by(ipmi_address=form.ipmi_address.data).all():
            flash(u'The current ipmi_address is already in use', 'error')
        elif form.ipmi_address.data != u'' and not validate_address(form.ipmi_address.data):
            flash(u'Incorrect ipmi_address', 'error')

        else:
            server = Server(form.group.data.id, form.desc.data, form.ext_address.data, form.int_address.data,
                            form.ipmi_address.data, form.other_address.data, form.idc.data, form.rack.data,
                            form.manufacturer.data, form.model.data, form.cpu_info.data, form.disk_info.data,
                            form.memory_info.data)
            db.session.add(server)
            db.session.commit()

            flash(u'Create server successfully', 'success')
            redirect_url = url_for('dashboard.list_server_ctrl')

        return redirect(redirect_url)


@dashboard.route('/server/<int:server_id>/edit', methods=("GET", "POST"))
@login_required
def edit_server_ctrl(server_id):

    user_access = UserAccessPermission('dashboard.edit_server_ctrl')
    if not user_access.can():
        abort(403)

    server = Server.query.filter_by(id=server_id).first()

    form = ServerForm(server)

    if request.method == 'GET':

        return render_template('dashboard/server_manager.html', form=form, type='create')

    elif request.method == 'POST':

        redirect_url = url_for('dashboard.edit_server_ctrl', server_id=server_id)

        if form.group.data is not None and form.group.data.id != server.group:
            if not Group.query.filter_by(id=form.group.data.id).all():
                flash(u'The current group is not exist', 'error')
                return  redirect(redirect_url)
            else:
                server.group = form.group.data.id

        if form.desc.data != u'' and form.desc.data != server.desc:
            server.desc = form.desc.data

        if form.ext_address.data != u'' and form.ext_address.data != server.ext_address:
            if Server.query.filter_by(ext_address=form.ext_address.data).all():
                flash(u'The current ext_address is exist', 'error')
                return  redirect(redirect_url)
            elif not validate_address(form.ext_address.data):
                flash(u'Incorrect ext_address', 'error')
                return  redirect(redirect_url)
            else:
                server.ext_address = form.ext_address.data

        if form.int_address.data != u'' and form.int_address.data != server.int_address:
            if Server.query.filter_by(int_address=form.int_address.data).all():
                flash(u'The current int_address is exist', 'error')
                return  redirect(redirect_url)
            elif not validate_address(form.int_address.data):
                flash(u'Incorrect int_address', 'error')
                return  redirect(redirect_url)
            else:
                server.int_address = form.int_address.data

        if form.ipmi_address.data != u'' and form.ipmi_address.data != server.ipmi_address:
            if Server.query.filter_by(ipmi_address=form.ipmi_address.data).all():
                flash(u'The current ipmi_address is exist', 'error')
                return  redirect(redirect_url)
            elif not validate_address(form.ipmi_address.data):
                flash(u'Incorrect ipmi_address', 'error')
                return  redirect(redirect_url)
            else:
                server.ipmi_address = form.ipmi_address.data

        if form.other_address.data != u'' and form.other_address.data != server.other_address:
            server.other_address = form.other_address.data

        if form.idc.data != u'' and form.idc.data != server.idc:
            server.idc = form.idc.data

        if form.rack.data != u'' and form.rack.data != server.rack:
            server.rack = form.rack.data

        if form.manufacturer.data != u'' and form.manufacturer.data != server.manufacturer:
            server.manufacturer = form.manufacturer.data

        if form.model.data != u'' and form.model.data != server.model:
            server.model = form.model.data

        if form.cpu_info.data != u'' and form.cpu_info.data != server.cpu_info:
            server.cpu_info = form.cpu_info.data

        if form.disk_info.data != u'' and form.disk_info.data != server.disk_info:
            server.disk_info = form.disk_info.data

        if form.memory_info.data != u'' and form.memory_info.data != server.memory_info:
            server.memory_info = form.memory_info.data

        else:
            server = Server(form.group.data.id, form.desc.data, form.ext_address.data, form.int_address.data,
                            form.ipmi_address.data, form.other_address.data, form.idc.data, form.rack.data,
                            form.manufacturer.data, form.model.data, form.cpu_info.data, form.disk_info.data,
                            form.memory_info.data)
            db.session.add(server)
            db.session.commit()

            flash(u'Edit server successfully', 'success')
            redirect_url = url_for('dashboard.list_server_ctrl')

        return redirect(redirect_url)


@dashboard.route('/acl/list')
@login_required
def list_acl_ctrl():

    user_access = UserAccessPermission('dashboard.list_acl_ctrl')
    if not user_access.can():
        abort(403)

    if request.method == 'GET':

        groups = Group.query.all()

        group_information = dict()
        for group in groups:
            group_information[unicode(group.id)] = group.desc

        access_control_dicts = dict()
        access_control_list = AccessControl.query.all()

        for access_control in access_control_list:

            function = access_control.function

            try:
                groups_access = json.loads(access_control.groups_access)
            except Exception, e:
                groups_access = dict()

            for group_id in groups_access:

                try:
                    access_control_dicts[group_id][function] = groups_access[group_id]
                except Exception:
                    access_control_dicts[group_id] = dict()
                    access_control_dicts[group_id][function] = groups_access[group_id]

        return render_template('dashboard/acl_manager.html', group_information=group_information,
                               access_control_dicts=access_control_dicts, type='list')


@dashboard.route('/acl/edit', methods=("GET", "POST"))
@login_required
def edit_acl_ctrl():

    user_access = UserAccessPermission('dashboard.edit_acl_ctrl')
    if not user_access.can():
        abort(403)

    form = AccessControlForm()

    if request.method == 'GET':

        return render_template('dashboard/acl_manager.html', form=form, type='edit')

    elif request.method == 'POST':

        redirect_url = url_for('dashboard.list_acl_ctrl')

        if not Group.query.filter_by(id=form.group.data.id).all():
            flash(u'The current group is not exist', 'error')
            return redirect(redirect_url)
        elif not AccessControl.query.filter_by(id=form.name.data.id).all():
            flash(u'The current function is not exist', 'error')
            return redirect(redirect_url)

        acl = AccessControl.query.filter_by(id=form.name.data.id).first()

        try:
            groups_access = json.loads(acl.groups_access)
        except Exception, e:
            groups_access = dict()

        groups_access[unicode(form.group.data.id)] = 1 if form.permission.data else 0

        acl.groups_access = json.dumps(groups_access)

        db.session.commit()

        flash(u'Edit ACL successfully', 'success')
        return redirect(redirect_url)