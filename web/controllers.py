#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    controllers.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).


from flask import render_template, request

from web import db
from web import app

from web.forms import UserLoginForm
from web.forms import CreateScriptRunnerOperateForm

from web.models import CreateScriptRunnerOperate


@app.route('/login', methods=['GET', 'POST'])
def user_login_ctrl():

    """
    登录页面
    """
    form = UserLoginForm()

    if request.method == 'GET':
        return  render_template('login.html', form=form)

    elif request.method == 'POST':

        return render_template('show_fucking.html', fucking=form.username.data)



@app.route('/operate/create', methods=("GET", "POST"))
def create_operate_ctrl():

    form = CreateScriptRunnerOperateForm()

    if request.method == 'POST':

        operate = CreateScriptRunnerOperate(0, form.server_list.data, form.command_list.data, form.variable_list.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('show_fucking.html', fucking=form.server_list.data)

    return render_template('operate/operate_create_undefined.html', form=form)