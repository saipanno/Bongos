#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/16.
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


import time
from sqlalchemy import exc, desc
from flask.ext.principal import UserNeed
from flask.ext.login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, Blueprint, json, Response, current_app

from frontend.forms.operation import CreatePingDetectForm, CreateSshDetectForm, CreateFabfileExecuteForm, \
    CreateCustomExecuteForm, CreatePowerCtrlForm

from frontend.models.account import User
from frontend.models.operation import OperationDb
from frontend.models.dashboard import SshConfig, FabricFile

from frontend.extensions.database import db
from frontend.extensions.principal import UserAccessPermission
from frontend.extensions.libs import catch_errors, format_address_list, format_ext_variables,\
    get_obj_attributes, get_dict_items

from application import backend_runner
from frontend.extensions.tasks import q


operation = Blueprint('operation', __name__, url_prefix='/operation')


@operation.route('/<operation_type>/list')
@login_required
def list_operation_ctrl(operation_type):

    access = UserAccessPermission('operation.list_operation_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    executes = OperationDb.query.filter_by(operation_type=operation_type).order_by(desc(OperationDb.id)).all()

    for execute in executes:
        user = User.query.filter_by(id=int(execute.author)).first()
        execute.author_name = user.name

    return render_template('operation/list_operation.html', executes=executes, operation_type=operation_type)


@operation.route('/<int:operation_id>/show')
@login_required
def show_operation_ctrl(operation_id):

    access = UserAccessPermission('operation.show_operation_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    default_next_page = request.values.get('next', url_for('account.index_ctrl'))

    try:
        execute = OperationDb.query.filter_by(id=operation_id).first()

    except exc.SQLAlchemyError:
        flash(u'Internal database error', 'error')
        return redirect(default_next_page)

    if execute is None:
        flash(u'The operating does not exist.', 'error')
        return redirect(default_next_page)

    try:
        fruits = json.loads(execute.result)
    except ValueError:
        fruits = dict()

    return render_template('operation/show_operation.html', execute=execute, fruits=fruits,
                           operation_type=execute.operation_type)


@operation.route('/<int:operation_id>/operation_export_result.csv')
@login_required
def export_operation_results_ctrl(operation_id):

    access = UserAccessPermission('operation.export_operation_results_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    try:
        execute = OperationDb.query.filter_by(id=operation_id).first()

    except exc.SQLAlchemyError:
        flash(u'Internal database error', 'error')
        return redirect(url_for('operation.list_operation_ctrl'))

    if execute is None:
        flash(u'The operating does not exist.', 'error')
        return redirect(url_for('operation.list_operation_ctrl'))

    try:
        fruits = json.loads(execute.result)
    except ValueError:
        fruits = dict()

    # Each yield expression is directly sent to the browser
    def create_result_csv():
        yield 'address,return code,message,error message\n'
        for address in fruits:
            yield '%s,%s,%s,%s\n' % \
                  (address, fruits[address].get('code', ''),
                   fruits[address].get('msg', ''), fruits[address].get('error', ''))

    return Response(create_result_csv(), mimetype='text/csv')


@operation.route('/ssh_detect/create', methods=("GET", "POST"))
@login_required
def create_ssh_detect_ctrl():

    access = UserAccessPermission('operation.create_ssh_detect_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    operation_type = u'ssh_status_detecting'

    form = CreateSshDetectForm()

    if request.method == 'GET':
        return render_template('operation/create_ssh_detecting.html', form=form, operation_type=operation_type)

    elif form.validate_on_submit():

        author = current_user.id
        datetime = time.strftime('%Y-%m-%d %H:%M')

        fruit = format_address_list(form.server_list.data)
        if fruit['status'] is not True:
            flash(fruit['desc'], 'error')
            return redirect(url_for('operation.create_ssh_detect_ctrl'))

        operation = OperationDb(author, datetime, operation_type, fruit['servers'],
                                u'', u'', form.ssh_config.data.id, 0, u'')
        db.session.add(operation)
        db.session.commit()

        ssh_config = SshConfig.query.filter_by(id=form.ssh_config.data.id).first()
        ssh_config_dict = get_obj_attributes(ssh_config, 'SSH')

        operations = get_obj_attributes(operation, 'OPT')
        operations.update(ssh_config_dict)

        q.enqueue(backend_runner, operations, get_dict_items(current_app.config, 'SETTINGS'))

        flash(u'Creating operation successfully', 'success')
        return redirect(url_for('operation.list_operation_ctrl', operation_type=operation_type))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('operation.create_ssh_detect_ctrl'))


@operation.route('/ping_detect/create', methods=("GET", "POST"))
@login_required
def create_ping_detect_ctrl():

    access = UserAccessPermission('operation.create_ping_detect_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    operation_type = u'ping_status_detecting'

    form = CreatePingDetectForm()

    if request.method == 'GET':
        return render_template('operation/create_ping_detecting.html', form=form, operation_type=operation_type)

    elif form.validate_on_submit():

        author = current_user.id
        datetime = time.strftime('%Y-%m-%d %H:%M')

        fruit = format_address_list(form.server_list.data)
        if fruit['status'] is not True:
            flash(fruit['desc'], 'error')
            return redirect(url_for('operation.create_ping_detect_ctrl'))

        operation = OperationDb(author, datetime, operation_type, fruit['servers'], u'', u'', 0, 0, u'')
        db.session.add(operation)
        db.session.commit()

        q.enqueue(backend_runner, get_obj_attributes(operation, 'OPT'), get_dict_items(current_app.config, 'SETTINGS'))

        flash(u'Creating operation successfully', 'success')
        return redirect(url_for('operation.list_operation_ctrl', operation_type=operation_type))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('operation.create_ping_detect_ctrl'))



@operation.route('/custom_execute/create', methods=("GET", "POST"))
@login_required
def create_custom_execute_ctrl():

    access = UserAccessPermission('operation.create_custom_execute_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    operation_type = u'custom_script_execute'

    form = CreateCustomExecuteForm()

    if request.method == 'GET':
        return render_template('operation/create_custom_script_execute.html', form=form, operation_type=operation_type)

    elif form.validate_on_submit():

        author = current_user.id
        datetime = time.strftime('%Y-%m-%d %H:%M')

        fruit = format_address_list(form.server_list.data)
        if fruit['status'] is not True:
            flash(fruit['desc'], 'error')
            return redirect(url_for('operation.create_custom_execute_ctrl'))

        ext_variables_dict = format_ext_variables(form.ext_variables.data)
        if ext_variables_dict['status'] is not True:
            flash(ext_variables_dict['desc'], 'error')
            return redirect(url_for('operation.create_custom_execute_ctrl'))
        ext_variables = json.dumps(ext_variables_dict['vars'], ensure_ascii=False)

        operation = OperationDb(author, datetime, operation_type, fruit['servers'], form.script_template.data,
                                ext_variables, form.ssh_config.data.id, 0, u'')
        db.session.add(operation)
        db.session.commit()

        ssh_config = SshConfig.query.filter_by(id=form.ssh_config.data.id).first()
        ssh_config_dict = get_obj_attributes(ssh_config, 'SSH')

        operations = get_obj_attributes(operation, 'OPT')
        operations.update(ssh_config_dict)

        q.enqueue(backend_runner, operations, get_dict_items(current_app.config, 'SETTINGS'))

        flash(u'Creating operation successfully', 'success')
        return redirect(url_for('operation.list_operation_ctrl', operation_type=operation_type))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('operation.create_custom_execute_ctrl'))


@operation.route('/fabfile_execute/create', methods=("GET", "POST"))
@login_required
def create_fabfile_execute_ctrl():

    access = UserAccessPermission('operation.create_fabfile_execute_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    operation_type = u'fabfile_execute'

    form = CreateFabfileExecuteForm()

    if request.method == 'GET':
        return render_template('operation/create_fabfile_execute.html', form=form, operation_type=operation_type)

    elif form.validate_on_submit():

        author = current_user.id
        datetime = time.strftime('%Y-%m-%d %H:%M')

        fruit = format_address_list(form.server_list.data)
        if fruit['status'] is not True:
            flash(fruit['desc'], 'error')
            return redirect(url_for('operation.create_fabfile_execute_ctrl'))

        ext_variables_dict = format_ext_variables(form.ext_variables.data)
        if ext_variables_dict['status'] is not True:
            flash(ext_variables_dict['desc'], 'error')
            return redirect(url_for('operation.create_fabfile_execute_ctrl'))
        ext_variables = json.dumps(ext_variables_dict['vars'], ensure_ascii=False)

        operation = OperationDb(author, datetime, operation_type, fruit['servers'], form.script_template.data.id,
                                ext_variables, form.ssh_config.data.id, 0, u'')
        db.session.add(operation)
        db.session.commit()

        ssh_config = SshConfig.query.filter_by(id=form.ssh_config.data.id).first()
        ssh_config_dict = get_obj_attributes(ssh_config, 'SSH')
        fabfile = FabricFile.query.filter_by(id=form.script_template.data.id).first()
        fabfile_dict = get_obj_attributes(fabfile, 'FABFILE')

        operations = get_obj_attributes(operation, 'OPT')
        operations.update(ssh_config_dict)
        operations.update(fabfile_dict)

        q.enqueue(backend_runner, operations, get_dict_items(current_app.config, 'SETTINGS'))

        flash(u'Creating operation successfully', 'success')
        return redirect(url_for('operation.list_operation_ctrl', operation_type=operation_type))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('operation.create_custom_execute_ctrl'))


@operation.route('/power_control/create', methods=("GET", "POST"))
@login_required
def create_power_control_ctrl():

    access = UserAccessPermission('operation.create_power_control_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    operation_type = u'remote_power_control'

    form = CreatePowerCtrlForm()

    if request.method == 'GET':
        return render_template('operation/create_power_control.html', form=form, operation_type=operation_type)

    elif form.validate_on_submit():

        author = current_user.id
        datetime = time.strftime('%Y-%m-%d %H:%M')

        fruit = format_address_list(form.server_list.data)
        if fruit['status'] is not True:
            flash(fruit['desc'], 'error')
            return redirect(url_for('operation.create_power_control_ctrl'))

        operation = OperationDb(author, datetime, operation_type, fruit['servers'],
                                form.script_template.data, u'', 0, 0, u'')
        db.session.add(operation)
        db.session.commit()

        q.enqueue(backend_runner, get_obj_attributes(operation, 'OPT'), get_dict_items(current_app.config, 'SETTINGS'))

        flash(u'Creating operation successfully', 'success')
        return redirect(url_for('operation.list_operation_ctrl', operation_type=operation_type))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('operation.create_power_control_ctrl'))
