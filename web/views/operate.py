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
from flask import render_template, request, redirect, url_for, flash, session
from sqlalchemy import desc

from web import db
from web import app

from web.forms.operate import CreatePingDetectForm
from web.forms.operate import CreateSshDetectForm
from web.forms.operate import CreatePreDefinedOperateForm
from web.forms.operate import CreateCustomOperateForm

from web.models.operate import SshDetect
from web.models.operate import PingDetect
from web.models.operate import PreDefinedOperate
from web.models.operate import CustomOperate


from web.extensions import login_required


@app.route('/detect/show')
@app.route('/detect/show/ping')
@login_required
def show_ping_detect_ctrl():

    if request.method == 'GET':

        detects = PingDetect.query.filter_by(author=session['user'].username).order_by(desc(PingDetect.id)).all()

        return render_template('operate/show_ping_detect.html', detects=detects)

@app.route('/detect/create', methods=("GET", "POST"))
@app.route('/detect/create/ping', methods=("GET", "POST"))
@login_required
def create_ping_detect_ctrl():

    form = CreatePingDetectForm()

    if request.method == 'GET':

        return render_template('operate/create_ping_detect.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'None':
            flash(u'Some input is None.', 'error')
            return redirect(url_for(''))
        else:
            detect = PingDetect(author, datetime, form.server_list.data)
            db.session.add(detect)
            db.session.commit()

            flash(u'Create detect successful.', 'success')
            return redirect(url_for('show_ping_detect_ctrl'))


@app.route('/detect/show/ssh')
@login_required
def show_ssh_detect_ctrl():

    if request.method == 'GET':

        detects = SshDetect.query.filter_by(author=session['user'].username).order_by(desc(SshDetect.id)).all()

        return render_template('operate/show_ssh_detect.html', detects=detects)

@app.route('/detect/create/ssh', methods=("GET", "POST"))
def create_ssh_detect_ctrl():

    form = CreateSshDetectForm()

    if request.method == 'GET':

        return  render_template('operate/create_ssh_detect.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'None' or form.ssh_config.data is None:
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_ssh_detect_ctrl'))
        else:
            detect = SshDetect(author, datetime, form.server_list.data, form.ssh_config.data.id)
            db.session.add(detect)
            db.session.commit()

            flash(u'Create detect successful.', 'success')

            return redirect(url_for('show_ssh_detect_ctrl'))


@app.route('/execute/show/predefined')
@login_required
def show_predefined_operate_ctrl():

    if request.method == 'GET':

        operates = PreDefinedOperate.query.filter_by(author=session['user'].username).order_by(desc(PreDefinedOperate.id)).all()

        return render_template('operate/show_predefined_operate.html', operates=operates)


@app.route('/execute/create/predefined', methods=("GET", "POST"))
@login_required
def create_predefined_operate_ctrl():

    form = CreatePreDefinedOperateForm()

    if request.method == 'GET':

        return render_template('operate/create_predefined_operate.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'None' or form.script_list.data is None or form.ssh_config.data is None:
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_predefined_operate_ctrl'))
        else:
            operate = PreDefinedOperate(author, datetime, form.server_list.data, form.script_list.data.id, form.template_vars.data, form.ssh_config.data.id)
            db.session.add(operate)
            db.session.commit()

            flash(u'Create operate successful.', 'success')
            return redirect(url_for('show_predefined_operate_ctrl'))


@app.route('/execute/show/custom')
@login_required
def show_custom_operate_ctrl():

    if request.method == 'GET':

        operates = CustomOperate.query.filter_by(author=session['user'].username).order_by(desc(CustomOperate.id)).all()

        return render_template('operate/show_custom_operate.html', operates=operates)


@app.route('/execute/create/custom', methods=("GET", "POST"))
@login_required
def create_custom_operate_ctrl():

    form = CreateCustomOperateForm()

    if request.method == 'GET':

        return  render_template('operate/create_custom_operate.html', form=form)

    elif request.method == 'POST':

        author = session['user'].username
        datetime = time.strftime('%Y-%m-%d %H:%M')

        if form.server_list.data == u'None' or form.template_script.data == u'None' or form.ssh_config.data is None:
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_custom_operate_ctrl'))
        else:
            operate = CustomOperate(author, datetime, form.server_list.data, form.template_script.data, form.template_vars.data, form.ssh_config.data.id)
            db.session.add(operate)
            db.session.commit()

            flash(u'Create operate successful.', 'success')

            return redirect(url_for('show_custom_operate_ctrl'))