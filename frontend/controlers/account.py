#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/17.
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
import os
from sqlalchemy import or_
from flask import render_template, request, flash, redirect, url_for, Blueprint, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from frontend.forms.account import UserLoginForm, EditSettingForm, ChangePasswordForm
from frontend.forms.dashboard import SshConfigForm, IpmiConfigForm, FabFileForm

from frontend.models.account import User, Group
from frontend.models.dashboard import SshConfig, IpmiConfig, FabFile

from frontend.extensions.database import db
from frontend.extensions.libs import catch_errors


account = Blueprint('account', __name__)


@account.route('/')
@login_required
def index_ctrl():

    return redirect(url_for('operation.list_operation_ctrl', operation_type='ping_connectivity_detecting'))


@account.route('/login', methods=['GET', 'POST'])
def user_login_ctrl():

    form = UserLoginForm()
    default_next_page = request.values.get('next', url_for('account.index_ctrl'))

    if request.method == 'GET':
        return render_template('account/user_login.html', form=form)

    elif request.method == 'POST' and form.validate():

        user = User.query.filter(or_(User.email == form.key_name.data, User.username == form.key_name.data)).first()

        if user is None:
            flash(u'User does not exist', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        elif not user.is_active():
            flash(u'User has been disabled', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        elif user.check_password(form.password.data):

            login_user(user)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

            flash(u'Login successfully', 'success')
            return redirect(default_next_page)

        else:
            flash(u'Current password is incorrect', 'error')
            return redirect(url_for('account.user_login_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.user_login_ctrl'))


@account.route('/logout')
def user_logout_ctrl():

    logout_user()

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('account.index_ctrl'))


@account.route('/settings/profile', methods=("GET", "POST"))
@login_required
def user_edit_settings_ctrl():

    user = current_user
    form = EditSettingForm(id=user.id, email=user.email, username=user.username, name=user.name)

    if request.method == 'GET':
        return render_template('account/change_settings.html', form=form)

    elif request.method == 'POST' and form.validate():

        if form.name.data != user.name:
            user.name = form.name.data

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

        return redirect(url_for('account.user_edit_settings_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.user_edit_settings_ctrl'))


@account.route('/settings/change_password', methods=("GET", "POST"))
@login_required
def user_change_password_ctrl():

    user = current_user
    form = ChangePasswordForm()

    if request.method == 'GET':
        return render_template('account/change_password.html', form=form)

    elif request.method == 'POST' and form.validate():

        if not user.check_password(form.now_password.data):
            flash(u'Current password is incorrect', 'error')
            return redirect(url_for('account.user_change_password_ctrl'))
        else:
            user.update_password(form.new_password.data)

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

        return redirect(url_for('account.user_change_password_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.user_change_password_ctrl'))

@account.route('/ssh_config/list')
@login_required
def list_ssh_config_ctrl():

    groups = current_user.groups.split(',')

    ssh_configs = list()
    all_ssh_configs = SshConfig.query.all()
    for ssh_config in all_ssh_configs:
        for group_id in ssh_config.groups.split(','):
            if group_id in groups:
                ssh_configs.append(ssh_config)

    for ssh_config in ssh_configs:
        user = User.query.filter_by(id=ssh_config.author).first()
        ssh_config.author_name = user.name

        groups_name = ''
        for group_id in ssh_config.groups.split(','):
            group = Group.query.filter_by(id=int(group_id)).first()
            groups_name = '%s, %s' % (groups_name, group.desc)
        ssh_config.groups_name = groups_name[2:]

    return render_template('account/ssh_config.html', ssh_configs=ssh_configs, type='list')


@account.route('/ssh_config/create', methods=("GET", "POST"))
@login_required
def create_ssh_config_ctrl():

    form = SshConfigForm()

    if request.method == 'GET':
        return render_template('account/ssh_config.html', form=form, type='create')

    elif request.method == 'POST' and form.validate():

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()

        ssh_config = SshConfig(form.username.data, form.desc.data, current_user.id, ','.join(groups), form.port.data,
                               form.username.data, form.password.data, form.private_key.data)
        db.session.add(ssh_config)
        db.session.commit()

        flash(u'Creating ssh configuration successfully', 'success')

        return redirect(url_for('account.list_ssh_config_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.create_ssh_config_ctrl'))


@account.route('/ssh_config/<int:config_id>/edit', methods=("GET", "POST"))
@login_required
def edit_ssh_config_ctrl(config_id):

    config = SshConfig.query.filter_by(id=config_id).first()

    if config.author != current_user.id:
        flash(u'Do not have permission to edit this config', 'error')
        return redirect(url_for('account.list_ssh_config_ctrl'))

    form = SshConfigForm(id=config.id, name=config.name, desc=config.desc, port=config.port, username=config.username,
                         private_key=config.private_key)

    if request.method == 'GET':
        return render_template('account/ssh_config.html', form=form, type='edit')

    elif request.method == 'POST' and form.validate():

        if form.name.data != config.name:
            config.name = form.name.data

        if form.desc.data != config.desc:
            config.desc = form.desc.data

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()
        config_groups = ','.join(groups)

        if config_groups != config.groups:
            config.groups = config_groups

        if form.port.data != config.port:
            config.port = form.port.data

        if form.username.data != config.username:
            config.username = form.username.data

        if form.password.data != config.password:
            config.password = form.password.data

        if form.private_key.data != config.private_key:
            config.private_key = form.private_key.data

        db.session.commit()

        flash(u'Edit ssh configuration successfully', 'success')
        return redirect(url_for('account.list_ssh_config_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.edit_ssh_config_ctrl', config_id=config_id))


@account.route('/ssh_config/<int:config_id>/delete')
@login_required
def delete_ssh_config_ctrl(config_id):

    config = SshConfig.query.filter_by(id=config_id).first()

    if config.author != current_user.id:
        flash(u'Do not have permission to delete this config', 'error')
        return redirect(url_for('account.list_ssh_config_ctrl'))

    # TODO:增加清理数据库环境操作

    db.session.delete(config)
    db.session.commit()

    flash(u'Delete ssh configuration successfully', 'success')
    return redirect(url_for('account.list_ssh_config_ctrl'))


@account.route('/ipmi_config/list')
@login_required
def list_ipmi_config_ctrl():

    groups = current_user.groups.split(',')

    ipmi_configs = list()
    all_ipmi_configs = IpmiConfig.query.all()
    for ssh_config in all_ipmi_configs:
        for group_id in ssh_config.groups.split(','):
            if group_id in groups:
                ipmi_configs.append(ssh_config)

    for ipmi_config in ipmi_configs:
        user = User.query.filter_by(id=ipmi_config.author).first()
        ipmi_config.author_name = user.name

        groups_name = ''
        for group_id in ssh_config.groups.split(','):
            group = Group.query.filter_by(id=int(group_id)).first()
            groups_name = '%s, %s' % (groups_name, group.desc)
        ssh_config.groups_name = groups_name[2:]

    return render_template('account/ipmi_config.html', ipmi_configs=ipmi_configs, type='list')


@account.route('/ipmi_config/create', methods=("GET", "POST"))
@login_required
def create_ipmi_config_ctrl():

    form = IpmiConfigForm()

    if request.method == 'GET':
        return render_template('account/ipmi_config.html', form=form, type='create')

    elif request.method == 'POST' and form.validate():

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()

        ipmi_config = IpmiConfig(form.username.data, form.desc.data, current_user.id, ','.join(groups),
                                 form.username.data, form.password.data, 1 if form.interface.data else 0)
        db.session.add(ipmi_config)
        db.session.commit()

        flash(u'Creating IPMI configuration successfully', 'success')

        return redirect(url_for('account.list_ipmi_config_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.create_ipmi_config_ctrl'))


@account.route('/ipmi_config/<int:config_id>/edit', methods=("GET", "POST"))
@login_required
def edit_ipmi_config_ctrl(config_id):

    config = IpmiConfig.query.filter_by(id=config_id).first()

    if config.author != current_user.id:
        flash(u'Do not have permission to edit this config', 'error')
        return redirect(url_for('account.list_ssh_config_ctrl'))

    form = IpmiConfigForm(id=config.id, name=config.name, desc=config.desc, username=config.username,
                          interface=True if config.interface else False)

    if request.method == 'GET':
        return render_template('account/ipmi_config.html', form=form, type='edit')

    elif request.method == 'POST' and form.validate():

        if form.name.data != config.name:
            config.name = form.name.data

        if form.desc.data != config.desc:
            config.desc = form.desc.data

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()
        config_groups = ','.join(groups)

        if config_groups != config.groups:
            config.groups = config_groups

        if form.username.data != config.username:
            config.username = form.username.data

        if form.password.data != config.password:
            config.password = form.password.data

        if form.interface.data or config.interface:
            config.interface = 1 if form.interface.data else 0

        db.session.commit()

        flash(u'Edit IPMI configuration successfully', 'success')
        return redirect(url_for('account.list_ipmi_config_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.edit_ipmi_config_ctrl', config_id=config_id))


@account.route('/ipmi_config/<int:config_id>/delete')
@login_required
def delete_ipmi_config_ctrl(config_id):

    config = IpmiConfig.query.filter_by(id=config_id).first()

    if config.author != current_user.id:
        flash(u'Do not have permission to delete this config', 'error')
        return redirect(url_for('account.list_ssh_config_ctrl'))

    # TODO:增加清理数据库环境操作

    db.session.delete(config)
    db.session.commit()

    flash(u'Delete IPMI configuration successfully', 'success')
    return redirect(url_for('account.list_ipmi_config_ctrl'))


@account.route('/fabfile/list')
@login_required
def list_fabfile_ctrl():

    groups = current_user.groups.split(',')

    fabfiles = list()
    all_fabfiles = FabFile.query.all()
    for fabfile in all_fabfiles:
        for group_id in fabfile.groups.split(','):
            if group_id in groups:
                fabfiles.append(fabfile)

    for fabfile in fabfiles:
        user = User.query.filter_by(id=fabfile.author).first()
        fabfile.author_name = user.name

        groups_name = ''
        for group_id in fabfile.groups.split(','):
            group = Group.query.filter_by(id=int(group_id)).first()
            groups_name = '%s, %s' % (groups_name, group.desc)
        fabfile.groups_name = groups_name[2:]

    return render_template('account/fabfile_manager.html', fabfiles=fabfiles, type='list')


@account.route('/fabfile/<int:fabfile_id>/show')
@login_required
def show_fabfile_ctrl(fabfile_id):

    default_next_page = request.values.get('next', url_for('account.index_ctrl'))

    fabfile = FabFile.query.filter_by(id=fabfile_id).first()

    if fabfile is None:
        flash(u'Fabfile does not exist', 'error')
        return redirect(default_next_page)

    with io.open(os.path.join(current_app.config['FABRIC_FILE_PATH'], '%s.py' % fabfile.name), mode='rt',
                 encoding='utf-8') as f:
        fabfile.script = f.read()

    return render_template('account/fabfile_manager.html', fabfile=fabfile, type='show')


@account.route('/fabfile/create', methods=("GET", "POST"))
@login_required
def create_fabfile_ctrl():

    form = FabFileForm()
    if request.method == 'GET':
        return render_template('account/fabfile_manager.html', form=form, type='create')

    elif request.method == 'POST' and form.validate():

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()

        with io.open(os.path.join(current_app.config['FABRIC_FILE_PATH'], '%s.py' % form.name.data), mode='wt',
                    encoding='utf-8') as f:
            f.write(form.script.data.replace('\r\n', '\n').replace('\r', '\n'))

        fabfile = FabFile(form.name.data, form.desc.data, current_user.id, ','.join(groups))
        db.session.add(fabfile)
        db.session.commit()

        flash(u'Create fabfile successfully', 'success')
        return redirect(url_for('account.list_fabfile_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.create_fabfile_ctrl'))


@account.route('/fabfile/<int:fabfile_id>/edit', methods=("GET", "POST"))
@login_required
def edit_fabfile_ctrl(fabfile_id):

    fabfile = FabFile.query.filter_by(id=fabfile_id).first()

    if fabfile.author != current_user.id:
        flash(u'Do not have permission to edit this fabfile', 'error')
        return redirect(url_for('account.list_ssh_config_ctrl'))

    with io.open(os.path.join(current_app.config['FABRIC_FILE_PATH'], '%s.py' % fabfile.name), mode='rt',
                 encoding='utf-8') as f:
        fabfile.script = f.read()

    form = FabFileForm(id=fabfile.id, name=fabfile.name, desc=fabfile.desc, script=fabfile.script)

    if request.method == 'GET':
        return render_template('account/fabfile_manager.html', form=form, type='edit')

    elif request.method == 'POST' and form.validate():

        with io.open(os.path.join(current_app.config['FABRIC_FILE_PATH'], '%s.py' % form.name.data), mode='wt',
                  encoding='utf-8') as f:
            f.write(form.script.data.replace('\r\n', '\n').replace('\r', '\n'))

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()
        config_groups = ','.join(groups)

        if config_groups != fabfile.groups:
            fabfile.groups = config_groups

        if form.desc.data != fabfile.desc:
            fabfile.desc = form.desc.data

        db.session.commit()

        flash(u'Edit fabfile successfully', 'success')
        return redirect(url_for('account.list_fabfile_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.create_fabfile_ctrl'))


@account.route('/fabfile/<int:fabfile_id>/delete')
@login_required
def delete_fabfile_ctrl(fabfile_id):

    fabfile = FabFile.query.filter_by(id=fabfile_id).first()

    if fabfile.author != current_user.id:
        flash(u'Do not have permission to delete this config', 'error')
        return redirect(url_for('account.list_fabfile_ctrl'))

    # TODO:增加清理数据库环境操作

    db.session.delete(fabfile)
    db.session.commit()

    flash(u'Edit idc successfully', 'success')
    return redirect(url_for('account.list_fabfile_ctrl'))