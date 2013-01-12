#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Briseis, An DataCenter Management.
#
#
#   Created at 2013/01/10. Ruoyan Wong(@saipanno).

from flask import render_template, request, url_for, flash, Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


class GetNodeGroupForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'服务器列表', id="textarea", description=u'需要远程执行命令的服务器列表,一行一个. 支持IP和域名.')
    command_list = TextAreaField(u'命令列表', id="textarea", description=u'需要远程执行的命令列表, 支持SHELL变量以及模板变量.')
    variable_list = TextAreaField(u'模板变量列表', id="textarea", description=u'模板变量列表.')

    submit = SubmitField(u'提交', id='submit', description='submit')

class LogIn(Form):
    pass

class Operate(db.Model):
    id = db.Column('operate_id', db.Integer, primary_key=True)
    operate_type   = db.Column(db.Integer)
    server_list    = db.Column(db.UnicodeText)
    command_list   = db.Column(db.UnicodeText)
    variable_list  = db.Column(db.UnicodeText)
    operate_status = db.Column(db.Integer)

    def __init__(self, operate_type, server_list, command_list, variable_list, operate_status=False):
        self.operate_type   = operate_type
        self.server_list    = server_list
        self.command_list   = command_list
        self.variable_list  = variable_list
        self.operate_status = operate_status

@app.route('/', methods=("GET", "POST"))
def InsertOperateInfo():

    form = GetNodeGroupForm(csrf_enabled=False)

    if request.method == 'POST':

        operate = Operate(0, form.server_list.data, form.command_list.data, form.variable_list.data)
        db.session.add(operate)
        db.session.commit()

        return render_template('show_fucking.html', fucking=form.server_list.data)

    return render_template('operate/operate_create.html', form=form)

@app.route('/login', methods=("GET", "POST"))
def Login():

    form = LogIn(csrf_enabled=False)
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])