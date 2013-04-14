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
from fabric.api import env, hide, execute

from web.models.operate import OperateDb
from web.models.dashboard import SshConfig

from application.modules.connectivity import ssh_connectivity_checking, ping_connectivity_checking


class Controller(object):

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

        self.operate.clear()

        operate_fetch = OperateDb.query.filter_by(status=u'0').first()

        if operate_fetch is not None:

            if operate_fetch.operate_type == u'Ping':

                self.operate['operate_type'] = u'Ping'
                self.operate['server_list'] = operate_fetch.server_list.split()

            elif operate_fetch.operate_type == u'Ssh':

                ssh_config_id = operate_fetch.ssh_config
                ssh_config = SshConfig.query.filter_by(id=int(ssh_config_id)).first()

                self.operate['operate_type'] = u'Ssh'
                self.operate['server_list'] = operate_fetch.server_list.split()
                self.operate['username'] = ssh_config.user
                self.operate['port'] = ssh_config.port
                self.operate['password'] = ssh_config.password
                self.operate['key_filename'] = ssh_config.key_filename

        # Operate_fetch为空时,直接返回空字典
        return self.operate

    def run(self):

        env.parallel = True
        env.warn_only = True

        env.pool_size = self.config.get('POOL_SIZE', 250)
        env.timeout = self.config.get('SSH_TIMEOUT', 30)
        env.command_timeout = self.config.get('SSH_COMMAND_TIMEOUT', 60)

        while 1:

            operate = self.get_operate_information()

            print operate

            operate_type = operate.get('operate_type', None)

            if operate_type is None:

                sleep(10)

            elif operate_type == u'Ping':

                with hide('stdout', 'stderr', 'running', 'aborts'):

                    output = execute(ping_connectivity_checking,
                                     self.config.get('PING_COUNT', 5),
                                     self.config.get('PING_TIMEOUT', 5),
                                     hosts=operate.get('server_list'))
                print output

            elif operate_type == u'Ssh':

                with hide('stdout', 'stderr', 'running', 'aborts'):

                    output = execute(ssh_connectivity_checking,
                                     operate,
                                     hosts=operate.get('server_list'))
                print output

            else:

                print 'Error Operate Type.'


            # debug mode, exit the loop
            break