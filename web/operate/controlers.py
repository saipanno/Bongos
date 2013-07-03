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
import json
from flask import render_template, request, redirect, url_for, flash, Blueprint
from sqlalchemy import desc
from flask.ext.login import login_required, current_user

from web import db

from web.operate.forms import CreatePingDetectForm, CreateSshDetectForm, CreatePreDefinedExecuteForm, \
    CreateCustomExecuteForm

from web.operate.models import OperateDb

from web.extensions import format_address_list
from web.extensions import format_template_vars


operate = Blueprint('operate', __name__, url_prefix='/operate')


@operate.route('/<operate_type>/list')
@login_required
def list_operate_ctrl(operate_type):

    executes = OperateDb.query.filter_by(operate_type=operate_type).order_by(desc(OperateDb.id)).all()

    return render_template('operate/list_operate.html', executes=executes, operate_type=operate_type)


@operate.route('/Ssh/create', methods=("GET", "POST"))
@login_required
def create_ssh_detect_ctrl():

    operate_type = u'Ssh'
    template_script = u'Ssh'
    template_vars = u'Ssh'
    status = u'0'
    result = u''

    form = CreateSshDetectForm()

    if request.method == 'GET':

        return  render_template('operate/create_ssh_detect.html', form=form)

    elif request.method == 'POST':

        author = current_user.name
        datetime = time.strftime('%Y-%m-%d %H:%M')

        server_list_dict = format_address_list(form.server_list.data)
        if server_list_dict['status'] is not True:
            flash(server_list_dict['desc'], 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        if form.ssh_config.data.id is None:
            flash(u'没有选择SSH配置', 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        journal = OperateDb(author, datetime, operate_type, server_list_dict['desc'], template_script,
                            template_vars, form.ssh_config.data.id, status, result)
        db.session.add(journal)
        db.session.commit()

        flash(u'成功创建操作.', 'success')
        return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))


@operate.route('/Ping/create', methods=("GET", "POST"))
@login_required
def create_ping_detect_ctrl():

    operate_type = u'Ping'
    template_script = u'Ping'
    template_vars = u'Ping'
    ssh_config = 0
    status = u'0'
    result = u''

    form = CreatePingDetectForm()

    if request.method == 'GET':

        return render_template('operate/create_ping_detect.html', form=form)

    elif request.method == 'POST':

        author = current_user.name
        datetime = time.strftime('%Y-%m-%d %H:%M')

        server_list_dict = format_address_list(form.server_list.data)
        if server_list_dict['status'] is not True:
            flash(server_list_dict['desc'], 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        journal = OperateDb(author, datetime, operate_type, server_list_dict['desc'], template_script,
                            template_vars, ssh_config, status, result)
        db.session.add(journal)
        db.session.commit()

        flash(u'成功创建操作.', 'success')
        return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))


@operate.route('/Custom/create', methods=("GET", "POST"))
@login_required
def create_custom_execute_ctrl():

    operate_type = u'Custom'
    status = u'0'
    result = u''

    form = CreateCustomExecuteForm()

    if request.method == 'GET':

        return  render_template('operate/create_custom_execute.html', form=form)

    elif request.method == 'POST':

        author = current_user.name
        datetime = time.strftime('%Y-%m-%d %H:%M')

        server_list_dict = format_address_list(form.server_list.data)
        if server_list_dict['status'] is not True:
            flash(server_list_dict['desc'], 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        if form.template_script == u'':
            flash(u'没有选择待执行脚本.', 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        if form.ssh_config.data.id is None:
            flash(u'没有选择SSH配置.', 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        template_vars_dict = format_template_vars(form.template_vars.data)
        if template_vars_dict['status'] is not True:
            flash(template_vars_dict['desc'], 'error')
            return redirect(url_for('operate.show_operate_ctrl', operate_type=operate_type))
        template_vars = json.dumps(template_vars_dict['desc'], ensure_ascii=False)

        journal = OperateDb(author, datetime, operate_type, server_list_dict['desc'], form.template_script.data,
                            template_vars, form.ssh_config.data.id, status, result)
        db.session.add(journal)
        db.session.commit()

        flash(u'成功创建操作.', 'success')
        return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))


@operate.route('/PreDefined/create', methods=("GET", "POST"))
@login_required
def create_predefined_execute_ctrl():

    operate_type = u'PreDefined'
    status = u'0'
    result = u''

    form = CreatePreDefinedExecuteForm()

    if request.method == 'GET':

        return  render_template('operate/create_predefined_execute.html', form=form)

    elif request.method == 'POST':

        author = current_user.name
        datetime = time.strftime('%Y-%m-%d %H:%M')

        server_list_dict = format_address_list(form.server_list.data)
        if server_list_dict['status'] is not True:
            flash(server_list_dict['desc'], 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        if form.template_script.data.id is None:
            flash(u'没有选择待执行脚本.', 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        if form.ssh_config.data.id is None:
            flash(u'没有选择SSH配置.', 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))

        template_vars_dict = format_template_vars(form.template_vars.data)
        if template_vars_dict['status'] is not True:
            flash(template_vars_dict['desc'], 'error')
            return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))
        template_vars = json.dumps(template_vars_dict['desc'], ensure_ascii=False)

        journal = OperateDb(author, datetime, operate_type, server_list_dict['desc'], form.template_script.data.id,
                            template_vars, form.ssh_config.data.id, status, result)
        db.session.add(journal)
        db.session.commit()

        flash(u'成功创建操作.', 'success')
        return redirect(url_for('operate.list_operate_ctrl', operate_type=operate_type))


@operate.route('/<int:operate_id>/show')
@login_required
def show_operate_ctrl(operate_id):

    execute = OperateDb.query.filter_by(id=operate_id).first()
    try:
        operate_result = json.loads(execute.result)
    except:
        operate_result = 0

    return render_template('operate/show_operate.html', execute=execute, operate_result=operate_result)
