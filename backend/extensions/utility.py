#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/04/24.
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


import re
import os

import settings


def generate_private_path(filename):

    if filename is not u'':
        return os.path.join(settings.PRIVATE_KEY_PATH, filename)
    else:
        return None


def analysis_script_output(output):

    # \S 匹配所有非空字符
    # +? 匹配前面正则一次或多次，非贪婪模式
    regexp = 'BD:\S+?:EOF'

    fruit = re.findall(regexp, output)

    # 字符串掐头去尾操作，删除BD:和:EOF
    return ' '.join(fruit[3:][:-4])


def generate_ipmi_address(address):

    fruit = address.split('.')

    return '%s.%s.%s' % (settings.IPMI_NETWORK, fruit[2], fruit[3])