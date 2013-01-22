#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    operate.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

import time

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import desc

from web import db
from web import app

from web.forms.operate import CreatePreDefinedOperateForm
from web.forms.operate import CreateCustomOperateForm

from web.models.operate import PreDefinedOperate
from web.models.operate import CustomOperate


@app.route('/operate/create', methods=("GET", "POST"))
@app.route('/operate/create/default', methods=("GET", "POST"))
def create_predefined_operate_ctrl():

    form = CreatePreDefinedOperateForm()

    if request.method == 'GET':

        return render_template('operate/create_predefined_operate.html', form=form)

    elif request.method == 'POST':

        author = 'wangruoyan'

        if form.server_list.data == u'None' or form.script_list.data is None or form.ssh_config.data is None:
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_predefined_operate_ctrl'))
        else:
            operate = PreDefinedOperate(author, time.strftime('%Y-%m-%d %H:%M'), form.server_list.data, form.script_list.data.id, form.ssh_config.data.id)
            db.session.add(operate)
            db.session.commit()

            flash(u'Create operate successful.', 'success')
            return redirect(url_for('show_predefined_operate_ctrl'))

@app.route('/operate/create/custom', methods=("GET", "POST"))
def create_custom_operate_ctrl():

    form = CreateCustomOperateForm()

    if request.method == 'GET':

        return  render_template('operate/create_custom_operate.html', form=form)

    elif request.method == 'POST':

        author = 'wangruoyan'

        if form.server_list.data == u'None' or form.template_script.data == u'None' or form.ssh_config.data is None:
            flash(u'Some input is None.', 'error')
            return redirect(url_for('show_custom_operate_ctrl'))
        else:
            operate = CustomOperate(author, time.strftime('%Y-%m-%d %H:%M'), form.server_list.data, form.template_script.data, form.template_vars.data, form.ssh_config.data.id)
            db.session.add(operate)
            db.session.commit()

            flash(u'Create operate successful.', 'success')

            return redirect(url_for('show_custom_operate_ctrl'))

@app.route('/operate/show')
@app.route('/operate/show/default')
def show_predefined_operate_ctrl():

    if request.method == 'GET':

        operates = PreDefinedOperate.query.order_by(desc(PreDefinedOperate.id)).all()

        return render_template('operate/show_predefined_operate.html', operates=operates)

@app.route('/operate/show/custom')
def show_custom_operate_ctrl():

    if request.method == 'GET':

        operates = CustomOperate.query.order_by(desc(CustomOperate.id)).all()

        return render_template('operate/show_custom_operate.html', operates=operates)