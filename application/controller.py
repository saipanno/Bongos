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
from fabric.api import env

from application.extensions import logger

from web.models.operate import OperateDb

from application.modules.ssh_connectivity import ssh_connectivity_checking
from application.modules.ping_connectivity import ping_connectivity_checking
from application.modules.custom_execute import custom_script_execute
from application.modules.predefined_execute import predefined_script_execute


class Controller(object):

    def __init__(self):

        self.config = dict()

    def config_from_object(self, obj):

        if isinstance(obj, basestring):
            obj = import_string(obj)

        for key in dir(obj):
            if key.isupper():
                self.config[key] = getattr(obj, key)

    def run(self):

        env.parallel = True
        env.warn_only = True

        env.pool_size = self.config.get('POOL_SIZE', 250)
        env.timeout = self.config.get('SSH_TIMEOUT', 30)
        env.command_timeout = self.config.get('SSH_COMMAND_TIMEOUT', 60)

        while 1:

            operate = OperateDb.query.filter_by(status=u'0').first()

            logger.info(u'Try to check for new tasks.')

            if operate is not None:

                if operate.operate_type == u'Ping':

                    ping_connectivity_checking(self.config, operate)

                elif operate.operate_type == u'Ssh':

                    ssh_connectivity_checking(self.config, operate)

                elif operate.operate_type == u'Custom':

                    custom_script_execute(self.config, operate)

                elif operate.operate_type == u'PreDefined':

                    print operate

                    predefined_script_execute(self.config, operate)

                else:

                    print 'Error Operate Type.'

            else:

                sleep(10)

            # debug mode, exit the loop
            break