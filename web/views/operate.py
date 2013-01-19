#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    operate.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

import time

from flask import render_template, request, redirect, url_for, flash
#from flask.ext.sqlalchemy import desc
from sqlalchemy import desc

from web import db
from web import app

from web.forms import CreateDefaultOperateForm
from web.forms import CreateCustomOperateForm

from web.models import OperateList
from web.models import RemoteScript
from web.models import SshConfig

@app.route('/operate/create', methods=("GET", "POST"))
@app.route('/operate/create/default', methods=("GET", "POST"))
def create_default_operate_ctrl():

    form = CreateDefaultOperateForm()

    if request.method == 'GET':

        return render_template('operate/operate_create_default.html', form=form)

    elif request.method == 'POST':

        operate_type = 0

        operate = OperateList(operate_type, time.strftime("%Y/%m/%d %H:%M"), form.server.data, form.script.data, form.ssh.data)
        db.session.add(operate)
        db.session.commit()

        flash(u'Create operate successful.', 'success')

        return redirect(url_for('show_default_operate_ctrl'))

@app.route('/operate/create/custom', methods=("GET", "POST"))
def create_custom_operate_ctrl():

    form = CreateCustomOperateForm()

    if request.method == 'GET':

        return  render_template('operate/operate_create_custom.html', form=form)

    elif request.method == 'POST':

        script_type = 1
        operate_type = 1

        script = RemoteScript(script_type, form.script.data, form.var.data)
        db.session.add(script)
        db.session.commit()

        script_id = 111

        operate = OperateList(operate_type, time.strftime("%Y/%m/%d %H:%M"), form.server.data, script_id, form.ssh.data)
        db.session.add(operate)
        db.session.commit()

        flash(u'Create operate successful.', 'success')

        return redirect(url_for('show_custom_operate_ctrl', status='success', message='Operate create successful.'))

@app.route('/operate/show')
@app.route('/operate/show/default')
def show_default_operate_ctrl():

    if request.method == 'GET':

        operates = OperateList.query.filter_by(type=0).order_by(desc(OperateList.id)).all()

        return render_template('operate/operate_show_default.html', operates=operates)

@app.route('/operate/show/custom')
def show_custom_operate_ctrl():

    if request.method == 'GET':

        operates = OperateList.query.filter_by(type=1).order_by(desc(OperateList.id)).all()

        return render_template('operate/operate_show_custom.html', operates=operates)