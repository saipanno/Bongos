#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/08/04.
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


from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_required

from frontend.extensions.database import db
from frontend.extensions.libs import catch_errors

from frontend.models.account import Group
from frontend.models.assets import Server, IDC

from frontend.forms.assets import ServerForm, IDCForm

from frontend.extensions.principal import UserAccessPermission


assets = Blueprint('assets', __name__, url_prefix='/assets')


@assets.route('/server/list')
@login_required
def list_server_ctrl():

    access = UserAccessPermission('assets.list_server_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    servers = Server.query.all()

    for server in servers:
        group_name = ''
        for group_id in server.groups.split(','):
            group = Group.query.filter_by(id=int(group_id)).first()
            group_name = '%s, %s' % (group_name, group.desc)
        server.group_name = group_name[2:]

        idc = IDC.query.filter_by(id=server.id).first()
        server.idc_name = idc.name

    return render_template('assets/server.html', servers=servers, type='list')


@assets.route('/server/create', methods=("GET", "POST"))
@login_required
def create_server_ctrl():

    access = UserAccessPermission('assets.create_server_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = ServerForm()

    if request.method == 'GET':

        return render_template('assets/server.html', form=form, type='create')

    elif request.method == 'POST' and form.validate():

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()

        server = Server(form.serial_number.data, form.assets_number.data, groups,
                        form.desc.data, form.ext_address.data, form.int_address.data, form.ipmi_address.data,
                        form.other_address.data, form.idc.data.id, form.rack.data, form.manufacturer.data,
                        form.model.data, form.cpu_info.data, form.disk_info.data, form.memory_info.data)
        db.session.add(server)
        db.session.commit()

        flash(u'Create server successfully', 'success')
        return redirect(url_for('assets.list_server_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('assets.create_server_ctrl'))


@assets.route('/server/<int:server_id>/edit', methods=("GET", "POST"))
@login_required
def edit_server_ctrl(server_id):

    access = UserAccessPermission('assets.edit_server_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    server = Server.query.filter_by(id=server_id).first()

    form = ServerForm(id=server.id, serial_number=server.serial_number, assets_number=server.assets_number,
                      desc=server.desc, ext_address=server.ext_address, int_address=server.int_address,
                      ipmi_address=server.ipmi_address, other_address=server.other_address, idc=server.idc,
                      rack=server.rack, manufacturer=server.manufacturer, model=server.model, cpu_info=server.cpu_info,
                      disk_info=server.disk_info, memory_info=server.memory_info)

    if request.method == 'GET':

        return render_template('assets/server.html', form=form, type='edit')

    elif request.method == 'POST' and form.validate():

        if form.serial_number.data != server.serial_number:
            server.serial_number = form.serial_number.data

        if form.assets_number.data != server.assets_number:
            server.assets_number = form.assets_number.data

        groups = list()
        for group in form.groups.data:
            groups.append(str(group.id))
        groups.sort()
        server_groups = ','.join(groups)
        if server_groups != server.groups:
            server.groups = server_groups

        if form.desc.data != server.desc:
            server.desc = form.desc.data

        if form.ext_address.data != server.ext_address:
            server.ext_address = form.ext_address.data

        if form.int_address != server.int_address:
            server.int_address = form.int_address.data

        if form.ipmi_address != server.ipmi_address:
            server.ipmi_address = form.ipmi_address.data

        if form.other_address != server.other_address:
            server.other_address = form.other_address.data

        if form.idc.data.id != server.idc:
            server.idc = form.idc.data.id

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

        db.session.commit()

        flash(u'Edit server successfully', 'success')
        return redirect(url_for('assets.list_server_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('assets.edit_server_ctrl', server_id=server_id))


@assets.route('/group/<int:server_id>/delete')
@login_required
def delete_server_ctrl(server_id):

    access = UserAccessPermission('assets.delete_server_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    server = Server.query.filter_by(id=server_id).first()

    db.session.delete(server)
    db.session.commit()

    flash(u'Edit server successfully', 'success')
    return redirect(url_for('assets.list_server_ctrl'))


@assets.route('/idc/list')
@login_required
def list_idc_ctrl():

    access = UserAccessPermission('assets.list_idc_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    idcs = IDC.query.all()

    return render_template('assets/datacenter.html', idcs=idcs, type='list')


@assets.route('/idc/create', methods=("GET", "POST"))
@login_required
def create_idc_ctrl():

    access = UserAccessPermission('assets.create_idc_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    form = IDCForm()

    if request.method == 'GET':

        return render_template('assets/datacenter.html', form=form, type='create')

    elif request.method == 'POST' and form.validate():

        group = IDC(form.name.data, form.desc.data, form.operators.data, form.address.data)
        db.session.add(group)
        db.session.commit()

        flash(u'Create IDC successfully', 'success')
        return redirect(url_for('assets.list_idc_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('assets.create_idc_ctrl'))


@assets.route('/idc/<int:idc_id>/edit', methods=("GET", "POST"))
@login_required
def edit_idc_ctrl(idc_id):

    access = UserAccessPermission('assets.edit_idc_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    idc = IDC.query.filter_by(id=idc_id).first()

    form = IDCForm(id=idc.id, name=idc.name, desc=idc.desc, operators=idc.operators, address=idc.address)

    if request.method == 'GET':

        return render_template('assets/datacenter.html', form=form, type='edit')

    elif request.method == 'POST' and form.validate():

        if form.name.data != idc.name:
            idc.name = form.name.data

        if form.operators.data != idc.operators:
            idc.operators = form.operators.data

        if form.address.data != idc.address:
            idc.address = form.address.data

        db.session.commit()

        flash(u'Edit IDC successfully', 'success')
        return redirect(url_for('assets.list_idc_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('assets.edit_idc_ctrl', idc_id=idc_id))


@assets.route('/group/<int:idc_id>/delete')
@login_required
def delete_idc_ctrl(idc_id):

    access = UserAccessPermission('assets.delete_idc_ctrl')
    if not access.can():
        flash(u'Don\'t have permission to this page', 'warning')
        return redirect(url_for('account.index_ctrl'))

    idc = IDC.query.filter_by(id=idc_id).first()

    # TODO:增加清理数据库环境操作

    db.session.delete(idc)
    db.session.commit()

    flash(u'Edit idc successfully', 'success')
    return redirect(url_for('assets.list_idc_ctrl'))

