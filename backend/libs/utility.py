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
from fabric.main import load_fabfile


def get_fab_tasks(fabfile_dir):

    fab_task_list = dict()

    if os.path.isdir(fabfile_dir):

        for fabfile in os.listdir(fabfile_dir):
            if fabfile.endswith('.py') and fabfile != '__init__.py':
                (docstring, task, default) = load_fabfile(fabfile)
                task_name = fabfile.replace('.py', '')
                fab_task_list[task_name] = task[task_name]

    return fab_task_list


def generate_private_path(filename, folder):

    if filename is not u'':
        return os.path.join(folder, filename)
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

    if address.startswith('122.11') or address.startswith('122.12'):
        return '%s.%s.%s' % ('192.168', fruit[2], fruit[3])
    elif address.startswith('10.178'):
        return '%s.%s.%s.%s' % (fruit[0], fruit[1], int(fruit[2])+1, fruit[3])
    else:
        return address