#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    base.py, in Briseis.
#
#
#    Created at 2013/01/17. Ruoyan Wong(@saipanno).

from flask import render_template, request

from web import app

from web.forms import UserLoginForm


@app.route('/', methods=['GET', 'POST'])
def index_ctrl():

    if request.method == 'GET':
        return  render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login_ctrl():

    form = UserLoginForm()

    if request.method == 'GET':
        return  render_template('login.html', form=form)