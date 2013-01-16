#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    controllers.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).


from flask import render_template, request, Blueprint

from web import db
from web import app

from web.forms import UserLoginForm

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/login', methods=['GET', 'POST'])
def UserLoginCtrl():

    form = UserLoginForm()

    if request.method == 'GET':
        return  render_template('login.html', form=form)

    elif request.method == 'POST':

        return render_template('show_fucking', fucking=form.password.data)



# @mod.route('/unDefineScript', methods=("GET", "POST"))
#def CreateDefinedScriptRunnerOperateCtrl():

#    form = CreateScriptRunnerOperateForm()

#    if request.method == 'POST':

#        operate = CreateScriptRunnerOperate(0, form.server_list.data, form.command_list.data, form.variable_list.data)
#        db.session.add(operate)
#        db.session.commit()

#        return render_template('show_fucking.html', fucking=form.server_list.data)

 #   return render_template('operate/operate_create_undefined.html', form=form)