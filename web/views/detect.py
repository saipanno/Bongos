#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/21.
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

from web.forms.detect import CreatePingDetectForm
from web.forms.detect import CreateSshDetectForm

from web.models.detect import SshDetect
from web.models.detect import PingDetect

from web.extensions import login_required


@app.route('/detect')
def index_detect_ctrl():

    if request.method == 'GET':

        return render_template('detect/detect_base.html')

@app.route('/detect/show')
@app.route('/detect/show/ping')
@login_required
def show_ping_detect_ctrl():

    if request.method == 'GET':

        detects = PingDetect.query.filter_by(author=session['user'].username).order_by(desc(PingDetect.id)).all()

        return render_template('detect/show_ping_detect.html', detects=detects)

@app.route('/detect/create', methods=("GET", "POST"))
@app.route('/detect/create/ping', methods=("GET", "POST"))
@login_required
def create_ping_detect_ctrl():

    form = CreatePingDetectForm()

    if request.method == 'GET':

        return render_template('detect/create_ping_detect.html', form=form)

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

        return render_template('detect/show_ssh_detect.html', detects=detects)

@app.route('/detect/create/ssh', methods=("GET", "POST"))
def create_ssh_detect_ctrl():

    form = CreateSshDetectForm()

    if request.method == 'GET':

        return  render_template('detect/create_ssh_detect.html', form=form)

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