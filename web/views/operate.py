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

from web.forms import OperateCreateDefaultForm
from web.forms import OperateCreateCustomForm

from web.models import OperateCreateDefineRunner


@app.route('/operate/create', methods=("GET", "POST"))
@app.route('/operate/create/default', methods=("GET", "POST"))
def create_default_operate_ctrl():

    form = OperateCreateDefaultForm()

    if request.method == 'GET':

        return render_template('operate/operate_create_default.html', form=form)

    elif request.method == 'POST':

        operate = OperateCreateDefineRunner(0, form.server_list.data, form.command_list.data, form.variable_list.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('show_fucking.html', fucking=form.server_list.data)

@app.route('/operate/create/custom', methods=("GET", "POST"))
def create_custom_operate_ctrl():

    form = OperateCreateCustomForm()

    if request.method == 'GET':

        return  render_template('operate/operate_create_custom.html', form=form)

    elif request.method == 'POST':

        operate = OperateCreateDefineRunner(0, form.server_list.data, form.command_list.data, form.variable_list.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('show_fucking.html', fucking=form.server_list.data)

@app.route('/operate/show')
@app.route('/operate/show/default')
def show_default_operate_ctrl():

    if request.method == 'GET':

        return render_template('operate/operate_show_default.html')

@app.route('/operate/show/custom')
def show_custom_operate_ctrl():

    if request.method == 'GET':

        return render_template('operate/operate_show_custom.html')