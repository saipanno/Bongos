#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/24.
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


from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, IntegerField


class CreatePreDefinedScriptForm(Form):

    script_desc = u'''用 <code>{{</code> 和 <code>}}</code> 作为外部变量的定界符,此类变量会依据变量文件中的定义进行替换, \
    同时模板依然支持shell中的 <code>$</code> 变量。 如：
<code>device=eth1; echo "IPADDR={{address}}"  >> ~/ifcfg-$device</code>'''

    name = TextField(u'Name<span class="required">*</span>', id='text', description=u'Script Name.')
    desc = TextAreaField(u'Description<span class="required">*</span>', id='text', description=u'Script Description.')
    script = TextAreaField(u'Script<span class="required">*</span>', id='textarea', description=script_desc)
    submit = SubmitField(u'Save', id='submit')


class CreateSshConfigForm(Form):

    name = TextField(u'Name<span class="required">*</span>', id='text', description=u'Config Name')
    desc = TextField(u'Description<span class="required">*</span>', id='text', description=u'Config Description')
    port = IntegerField(u'Port<span class="required">*</span>', id='port', description=u'Ssh Server Port.', default=22)
    username = TextField(u'Username<span class="required">*</span>', id='text')
    password = TextField(u'Password<span class="required">*</span>', id='text')
    private_key = TextField(u'Secret Key<span class="required">*</span>:', id='text',
                             description=u'The Path of Secret Key')
    submit = SubmitField(u'Save', id='submit')