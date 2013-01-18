#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    basic.py, in Briseis.
#
#
#    Created at 2013/01/17. Ruoyan Wong(@saipanno).

from flask import render_template, request

from web import db
from web import app

from web.forms import UserLoginForm

@app.route('/', methods=['GET', 'POST'])
def index_ctrl():

    if request.method == 'GET':
        return  render_template('index.html')


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