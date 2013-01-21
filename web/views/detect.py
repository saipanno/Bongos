#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    detect.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

import time

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import desc

from web import db
from web import app

from web.forms.detect import CreatePingDetectForm
from web.forms.detect import CreateSshDetectForm

from web.models.detect import Detect

@app.route('/detect/show')
@app.route('/detect/show/ping')
def show_ping_detect_ctrl():

    if request.method == 'GET':

        detects = Detect.query.filter_by(type=0).order_by(desc(Detect.id)).all()

        return render_template('detect/show_ping_detect.html', detects=detects)

@app.route('/detect/create', methods=("GET", "POST"))
@app.route('/detect/create/ping', methods=("GET", "POST"))
def create_ping_detect_ctrl():

    form = CreatePingDetectForm()

    if request.method == 'GET':

        return render_template('detect/create_ping_detect.html', form=form)

    elif request.method == 'POST':

        author = 'wangruoyan'
        detect_type = 0

        if form.server_list.data == u'None':
            flash(u'Some input is None.', 'error')
            return redirect(url_for(''))
        else:
            detect = Detect(detect_type, author, time.strftime('%Y-%m-%d %H:%M'), form.server_list.data, u'None')
            db.session.add(detect)
            db.session.commit()

            flash(u'Create detect successful.', 'success')
            return redirect(url_for('show_ping_detect_ctrl'))


@app.route('/detect/show/ssh')
def show_ssh_detect_ctrl():

    if request.method == 'GET':

        detects = Detect.query.filter_by(type=1).order_by(desc(Detect.id)).all()

        return render_template('detect/show_ssh_detect.html', detects=detects)

@app.route('/detect/create/ssh', methods=("GET", "POST"))
def create_ssh_detect_ctrl():

    form = CreateSshDetectForm()

    if request.method == 'GET':

        return  render_template('detect/create_ssh_detect.html', form=form)

    elif request.method == 'POST':

        author = 'wangruoyan'
        detect_type = 1

        if form.server_list.data == u'None' or form.ssh_config.data == u'None':
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_ssh_detect_ctrl'))
        else:
            detect = Detect(detect_type, author, time.strftime('%Y-%m-%d %H:%M'), form.server_list.data, form.ssh_config.data)
            db.session.add(detect)
            db.session.commit()

            flash(u'Create detect successful.', 'success')

            return redirect(url_for('show_ssh_detect_ctrl'))