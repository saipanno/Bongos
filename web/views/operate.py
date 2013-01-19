#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    operate.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).


from flask import render_template, request

from web import db
from web import app

from web.forms import CreateDefaultOperateForm
from web.forms import CreateCustomOperateForm

from web.models import CreateOperateRunner

@app.route('/operate/create', methods=("GET", "POST"))
@app.route('/operate/create/default', methods=("GET", "POST"))
def create_default_operate_ctrl():

    form = CreateDefaultOperateForm()

    if request.method == 'GET':

        return render_template('operate/operate_create_default.html', form=form)

    elif request.method == 'POST':

        operate = CreateOperateRunner(0, form.server.data, form.script.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('operate/operate_show_default.html', status='success', message='Operate create successful.')

@app.route('/operate/create/custom', methods=("GET", "POST"))
def create_custom_operate_ctrl():

    form = CreateCustomOperateForm()

    if request.method == 'GET':

        return  render_template('operate/operate_create_custom.html', form=form)

    elif request.method == 'POST':

        operate = CreateOperateRunner(1, form.server.data, form.script.data, form.var.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('operate/operate_show_custom.html', status='success', message='Operate create successful.')

@app.route('/operate/show')
@app.route('/operate/show/default')
def show_default_operate_ctrl():

    if request.method == 'GET':

        operates = CreateOperateRunner.query.filter_by(type=0).all()

        return render_template('operate/operate_show_default.html', operates=operates)

@app.route('/operate/show/custom')
def show_custom_operate_ctrl():

    if request.method == 'GET':

        operates = CreateOperateRunner.query.filter_by(type=1).all()

        return render_template('operate/operate_show_custom.html', operates=operates)