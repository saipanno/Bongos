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


from flask.ext.wtf import Form, TextAreaField, HiddenField, SubmitField, QuerySelectField

from web.dashboard.models import SshConfig, PreDefinedScript


class CreateSshDetectForm(Form):

    next_page = HiddenField()
    server_list = TextAreaField(u'Server List<span class="required">*</span>', id='textarea',
                                description=u'Support IP Address.')
    ssh_config = QuerySelectField(u'Ssh Config<span class="required">*</span>', id='select',
                                  description=u'Ssh Config', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Save', id='submit')


class CreatePingDetectForm(Form):

    next_page = HiddenField()
    server_list = TextAreaField(u'Server List<span class="required">*</span>', id='textarea',
                                description=u'Support IP Address.')
    submit = SubmitField(u'Save', id='submit')


class CreatePreDefinedExecuteForm(Form):

    vars_desc = u'''<p>用 <code>|</code> 作为key(IP地址)和value的分隔符, 用 <code>,</code> 作为value(多个变量赋值)的分隔符, \
    用 <code>=</code> 作为单变量的赋值符。 如:</p>
<code>60.175.193.194|address=61.132.226.195,gateway=61.132.226.254</code>'''

    next_page = HiddenField()
    server_list = TextAreaField(u'Server List<span class="required">*</span>', id='textarea',
                                description=u'Support IP Address.')
    script_template = QuerySelectField(u'PreDefined Script<span class="required">*</span>', id='select',
                                       description=u'Select PreDefined Script.',
                                       query_factory=PreDefinedScript.query.all, get_label='desc')
    template_vars = TextAreaField(u'External Variables<span class="required">*</span>', id='textarea',
                                  description=vars_desc)
    ssh_config = QuerySelectField(u'Ssh Config<span class="required">*</span>', id='select',
                                  description=u'Ssh Config', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Save', id='submit')


class CreateCustomExecuteForm(Form):

    script_desc = u'''用 <code>{{</code> 和 <code>}}</code> 作为外部变量的定界符,此类变量会依据变量文件中的定义进行替换, \
    同时模板依然支持shell中的 <code>$</code> 变量。 如：
<code>device=eth1; echo "IPADDR={{address}}"  >> ~/ifcfg-$device</code>'''

    vars_desc = u'''用 <code>|</code> 作为key(IP地址)和value的分隔符, 用 <code>,</code> 作为value(多个变量赋值)的分隔符, \
    用 <code>=</code> 作为单变量的赋值符。 如:
<code>60.175.193.194|address=61.132.226.195,gateway=61.132.226.254</code>'''

    next_page = HiddenField()
    server_list = TextAreaField(u'Server List<span class="required">*</span>', id='textarea',
                                description=u'Support IP Address.')
    script_template = TextAreaField(u'Script<span class="required">*</span>', id='textarea', description=script_desc)
    template_vars = TextAreaField(u'External Variables<span class="required">*</span>', id='textarea',
                                  description=vars_desc)
    ssh_config = QuerySelectField(u'Ssh Config<span class="required">*</span>', id='select',
                                  description=u'Ssh Config', query_factory=SshConfig.query.all,  get_label='desc')
    submit = SubmitField(u'Save', id='submit')