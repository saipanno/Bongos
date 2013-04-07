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

from flask import render_template, request, redirect, url_for, flash, session
from sqlalchemy import desc

from web import db
from web import app

from web.forms.operate import CreatePingDetectForm
from web.forms.operate import CreateSshDetectForm
from web.forms.operate import CreatePreDefinedExecuteForm
from web.forms.operate import CreateCustomExecuteForm

from web.models.operate import SshDetect
from web.models.operate import PreDefinedExecute
from web.models.operate import CustomExecute
from web.models.operate import Execute

from web.extensions import login_required


@app.route('/detect/show/<style>')
@login_required
def show_detect_ctrl(style):

    executes = Execute.query.filter_by(style=style).order_by(desc(Execute.id)).all()
    return render_template('operate/show_detect.html', executes=executes, style=style)


@app.route('/detect/create/ping', methods=("GET", "POST"))
@login_required
def create_ping_detect_ctrl():

    form = CreatePingDetectForm()

    if request.method == 'GET':

        return render_template('operate/create_ping_detect.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'':

            flash(u'Some input is empty.', 'error')
            return redirect(url_for('show_detect_ctrl', style='Ping'))

        style = 'PingDetect'
        server_list = form.server_list.data
        template_script = 'PingDetect'
        template_vars = 'PingDetect'
        ssh_config = 0
        status = 'Waiting'

        journal = Execute(author, datetime, style, server_list, template_script, template_vars, ssh_config, status)
        db.session.add(journal)
        db.session.commit()

        flash(u'Create detect successful.', 'success')
        return redirect(url_for('show_detect_ctrl', style='Ping'))


@app.route('/detect/create/ssh', methods=("GET", "POST"))
def create_ssh_detect_ctrl():

    form = CreateSshDetectForm()

    if request.method == 'GET':

        return  render_template('operate/create_ssh_detect.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'' or form.ssh_config.data is None:
            flash(u'Some input is empty.', 'error')
            return redirect(url_for('show_detect_ctrl', style='Ssh'))
        else:
            detect = SshDetect(author, datetime, form.server_list.data, form.ssh_config.data.id)
            db.session.add(detect)
            db.session.commit()

            flash(u'Create detect successful.', 'success')

            return redirect(url_for('show_detect_ctrl', style='Ssh'))


@app.route('/execute/create/PreDefined', methods=("GET", "POST"))
@login_required
def create_predefined_execute_ctrl():

    form = CreatePreDefinedExecuteForm()

    if request.method == 'GET':

        return render_template('operate/create_predefined_execute.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'' or form.script_list.data is None or form.ssh_config.data is None:
            flash(u'Some input is empty.', 'error')
            return redirect(url_for('show_detect_ctrl', style='PreDefined'))
        else:
            operate = PreDefinedExecute(author, datetime, form.server_list.data, form.script_list.data.id,
                                        form.template_vars.data, form.ssh_config.data.id)
            db.session.add(operate)
            db.session.commit()

            flash(u'Create execute successful.', 'success')
            return redirect(url_for('show_detect_ctrl', style='PreDefined'))


@app.route('/execute/create/Custom', methods=("GET", "POST"))
@login_required
def create_custom_execute_ctrl():

    form = CreateCustomExecuteForm()

    if request.method == 'GET':

        return  render_template('operate/create_custom_execute.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'' or form.template_script.data == u'None' or form.ssh_config.data is None:
            flash(u'Some input is empty.', 'error')
            return redirect(url_for('show_detect_ctrl', style='Custom'))
        else:
            operate = CustomExecute(author, datetime, form.server_list.data, form.template_script.data,
                                    form.template_vars.data, form.ssh_config.data.id)
            db.session.add(operate)
            db.session.commit()

            flash(u'Create execute successful.', 'success')

            return redirect(url_for('show_detect_ctrl', style='Custom'))
