#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/16.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, QuerySelectField, SelectField, Required

from frontend.models.dashboard import SshConfig, PreDefinedScript


class CreateSshDetectForm(Form):

    next_page = HiddenField()

    server_list = TextAreaField(u'Server List', description=u'Only support ip address. \
    Separated by <code>;</code>、<code>,</code>、<code>空格</code> and <code>换行</code>',
                                validators=[Required(message=u'Server list is required')])
    ssh_config = QuerySelectField(u'Ssh Config', query_factory=SshConfig.query.all, get_label='desc',
                                  validators=[Required(message=u'Ssh config is required')])

    submit = SubmitField(u'Submit', id='submit')


class CreatePingDetectForm(Form):

    next_page = HiddenField()

    server_list = TextAreaField(u'Server List', description=u'Only support ip address. \
    Separated by <code>;</code>、<code>,</code>、<code>空格</code> and <code>换行</code>',
                                validators=[Required(message=u'Server list is required')])

    submit = SubmitField(u'Submit', id='submit')


class CreateCustomExecuteForm(Form):

    script_desc = u'''作为shell中的 <code>$</code> 内部变量的扩展，模板还支持外部变量。\
    <code>{{</code> 和 <code>}}</code> 作为外部变量的定界符,此类变量会依据变量文件中的同名赋值定义进行替换, \
    同时标准错误输出以及标准输出中匹配到<code>BD:\w+?:EOF</code>的字符串可以作为返回结果保存。如：
<code>device=eth1; echo "IPADDR={{address}}"  >> ~/ifcfg-$device</code>'''

    vars_desc = u'''用 <code>|</code> 作为key(IP地址)和value的分隔符, 用 <code>,</code> 作为value(多个变量赋值)的分隔符, \
    用 <code>=</code> 作为单变量的赋值符。 如:
<code>60.175.193.194|address=61.132.226.195,gateway=61.132.226.254</code>'''

    next_page = HiddenField()

    server_list = TextAreaField(u'Server List', description=u'Only support ip address. \
    Separated by <code>;</code>、<code>,</code>、<code>空格</code> and <code>换行</code>',
                                validators=[Required(message=u'Server list is required')])
    script_template = TextAreaField(u'Script Template', description=script_desc,
                                    validators=[Required(message=u'Script Template is required')])
    template_vars = TextAreaField(u'External Variables', description=vars_desc)
    ssh_config = QuerySelectField(u'Ssh Config', query_factory=SshConfig.query.all, get_label='desc',
                                  validators=[Required(message=u'Ssh config is required')])

    submit = SubmitField(u'Submit', id='submit')


class CreatePreDefinedExecuteForm(Form):

    vars_desc = u'''<p>用 <code>|</code> 作为key(IP地址)和value的分隔符, 用 <code>,</code> 作为value(多个变量赋值)的分隔符, \
    用 <code>=</code> 作为单变量的赋值符。 如:</p>
<code>60.175.193.194|address=61.132.226.195,gateway=61.132.226.254</code>'''

    next_page = HiddenField()

    server_list = TextAreaField(u'Server List', description=u'Only support ip address. \
    Separated by <code>;</code>、<code>,</code>、<code>空格</code> and <code>换行</code>',
                                validators=[Required(message=u'Server list is required')])
    script_template = QuerySelectField(u'PreDefined Script', description=u'PreDefined Script.',
                                       query_factory=PreDefinedScript.query.all, get_label='desc',
                                       validators=[Required(message=u'Script Template is required')])
    template_vars = TextAreaField(u'External Variables', description=vars_desc)
    ssh_config = QuerySelectField(u'Ssh Config', query_factory=SshConfig.query.all, get_label='desc',
                                  validators=[Required(message=u'Ssh config is required')])

    submit = SubmitField(u'Submit', id='submit')


class CreatePowerCtrlForm(Form):

    next_page = HiddenField()

    server_list = TextAreaField(u'Server List', description=u'Only support ip address. \
    Separated by <code>;</code>、<code>,</code>、<code>空格</code> and <code>换行</code>',
                                validators=[Required(message=u'Server list is required')])
    script_template = SelectField(u'Operate Type', description=u'Power operate type, support by `ipmitool`',
                                  choices=[(u'reset', u'重启'), (u'off', u'关机'), (u'on', u'开机'), (u'status', u'状态')])

    submit = SubmitField(u'Submit', id='submit')