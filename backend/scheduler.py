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


import time
from werkzeug.utils import import_string
from fabric.api import env

from backend.extensions.database import db
from backend.extensions.logger import logger

from backend.models import OperationDb

from backend.plugins.ssh_connectivity import ssh_connectivity_checking
from backend.plugins.ping_connectivity import ping_connectivity_checking
from backend.plugins.custom_execute import custom_script_execute
from backend.plugins.predefined_execute import predefined_script_execute
from backend.plugins.remote_power_control import exec_power_management


class Scheduler(object):

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
        env.disable_known_hosts = self.config.get('DISABLE_KNOWN_HOSTS', True)

        while True:

            operation = db.query(OperationDb).filter_by(status=u'0').first()

            if operation is not None:

                logger.info('Started a new operating unit. ID: %s, TYPE: %s, HOSTS: %s' %
                            (operation.id, operation.operation_type, operation.server_list))

                if operation.operation_type == u'ping_detect':
                    ping_connectivity_checking(self.config, operation)

                elif operation.operation_type == u'ssh_detect':
                    ssh_connectivity_checking(operation)

                elif operation.operation_type == u'custom_execute':
                    custom_script_execute(operation)

                elif operation.operation_type == u'predefined_execute':
                    predefined_script_execute(operation)

                elif operation.operation_type == u'power_control':
                    exec_power_management(self.config, operation)

                else:
                    logger.error('Wrong type of operation. ID: %s, TYPE: %s' % (operation.id, operation.operation_type))

            else:

                time.sleep(10)

            #break