#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/04/02.
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


from time import sleep
from werkzeug.utils import import_string
from fabric.api import env, hide, show, execute

from web.models.operate import OperateDB
from application.module.connectivity import ssh_connectivity_checking, ping_connectivity_checking


class Briseis(object):

    def __init__(self):

        self.config = dict()
        self.operate = dict()

    def config_from_object(self, obj):

        if isinstance(obj, basestring):
            obj = import_string(obj)

        for key in dir(obj):
            if key.isupper():
                self.config[key] = getattr(obj, key)

    def get_operate_information(self):

        # TODO: 增加实际操作单信息获取逻辑。

        self.operate.clear()

        #operate = {'hosts': ['122.11.45.162', '122.11.45.38', '122.11.45.126', '122.11.45.157'],
        #           'type': 'ping_connectivity_checking'}

        operate = {'type': 'ssh_connectivity_checking',
                   'hosts': ['122.11.45.162', '122.11.45.38', '122.11.45.126', '122.11.45.157'],
                   'user': 'root',
                   'port': 22,
                   'password': 'hello.com',
                   'key_filename': '~/.ssh/ku_rsa'}

        return operate

    def run(self):

        env.parallel = True
        env.warn_only = True

        env.pool_size = self.config.get('POOL_SIZE', 250)
        env.timeout = self.config.get('SSH_TIMEOUT', 30)
        env.command_timeout = self.config.get('SSH_COMMAND_TIMEOUT', 60)

        while 1:

            operate = self.get_operate_information()

            operate_type = operate.get('type', None)

            if operate_type is None:

                sleep(10)

            elif operate_type == 'ping_connectivity_checking':

                with show('stdout', 'stderr', 'running'):

                    output = execute(ping_connectivity_checking,
                                     self.config.get('PING_COUNT', 5),
                                     self.config.get('PING_TIMEOUT', 5),
                                     hosts=operate.get('hosts'))
                print output

            elif operate_type == 'ssh_connectivity_checking':

                with show('stdout', 'stderr', 'running', 'aborts'):

                    output = execute(ssh_connectivity_checking,
                                     operate,
                                     hosts=operate.get('hosts'))
                print output

            else:

                print 'Error Operate Type.'


            # debug mode, exit the loop
            break