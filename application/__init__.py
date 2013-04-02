#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/02/22.
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
from fabric.api import env, hide, show, execute

from application.extensions import config_from_object, get_operate_information

from application.module.connectivity import ssh_connectivity_checking, ping_connectivity_checking


def main():

    env.parallel = True
    env.warn_only = True

    config = config_from_object('settings')

    env.pool_size = config.get('POOL_SIZE', 250)
    env.timeout = config.get('SSH_TIMEOUT', 30)
    env.command_timeout = config.get('SSH_COMMAND_TIMEOUT', 60)

    while 1:

        # operate = get_operate_information()

        #operate = {'hosts': ['122.11.45.162', '122.11.45.38', '122.11.45.126', '122.11.45.157'],
        #           'type': 'ping_connectivity_checking'}
        operate = {'type': 'ssh_connectivity_checking',
                   'hosts': ['122.11.45.162', '122.11.45.38', '122.11.45.126', '122.11.45.157'],
                   'user': 'root',
                   'port': 22,
                   'password': 'hello.com',
                   'key_filename': '~/.ssh/ku_rsa'}

        operate_type = operate.get('type', None)

        if operate_type is None:

            sleep(10)

        elif operate_type == 'ping_connectivity_checking':

            with show('stdout', 'stderr', 'running'):

                output = execute(ping_connectivity_checking,
                                 config.get('PING_COUNT', 5),
                                 config.get('PING_TIMEOUT', 5),
                                 hosts=operate.get('hosts'))
                print output

        elif operate_type == 'ssh_connectivity_checking':

            with show('stdout', 'stderr', 'running', 'aborts'):

                output = execute(ssh_connectivity_checking,
                                 operate,
                                 config.get('SSH_TIMEOUT', 30),
                                 config.get('SSH_COMMAND_TIMEOUT', 60),
                                 hosts=operate.get('hosts'))
                print output

        else:

            print 'Error Operate Type.'

        # debug mode, exit the loop
        break
