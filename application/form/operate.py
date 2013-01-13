#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    oprate.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, SelectField

class CreateDefinedScriptRunnerOperateForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'服务器列表', id='textarea', description=u'需要远程执行命令的服务器列表,一行一个. 支持IP和域名.')
    script_type = SelectField(u'脚本列表', id='select', description=u'预定义的脚本列表.')

    submit = SubmitField(u'提交', id='submit', description='submit')

class CreateScriptRunnerOperateForm(Form):

    next = HiddenField()
    server_list = TextAreaField(u'服务器列表', id='textarea', description=u'需要远程执行命令的服务器列表,一行一个. 支持IP和域名.')
    command_list = TextAreaField(u'命令列表', id='textarea', description=u'需要远程执行的命令列表, 支持SHELL变量以及模板变量.')
    variable_list = TextAreaField(u'模板变量列表', id='textarea', description=u'模板变量列表.')

    submit = SubmitField(u'提交', id='submit', description='submit')