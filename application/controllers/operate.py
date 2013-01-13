#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    operate.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

from flask import render_template, request, Blueprint

from application import db

from application.models.operate import CreateScriptRunnerOperate
from application.form.operate import CreateScriptRunnerOperateForm

mod = Blueprint('operate', __name__, url_prefix='/operate')

@mod.route('/unDefineScript', methods=("GET", "POST"))
def CreateDefinedScriptRunnerOperateCtrl():

    form = CreateScriptRunnerOperateForm()

    if request.method == 'POST':

        operate = CreateScriptRunnerOperate(0, form.server_list.data, form.command_list.data, form.variable_list.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('show_fucking.html', fucking=form.server_list.data)

    return render_template('operate/operate_create_undefined.html', form=form)