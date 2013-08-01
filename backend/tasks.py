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


import sys
from fabric.api import env

from backend.extensions.logger import logger

from backend.extensions.libs import get_fab_tasks

from backend.operations.ssh_status_detecting import ssh_status_detecting
from backend.operations.ping_status_detecting import ping_status_detecting
from backend.operations.custom_script_execute import custom_script_execute
#from backend.operations.predefined_fabfile_execute import predefined_fabfile_execute
from backend.operations.remote_power_control import remote_power_control


def backend_runner(operation=None, config=None):

    env.parallel = True
    env.warn_only = True

    env.timeout = config.get('SETTINGS_SSH_TIMEOUT', 30)
    env.pool_size = config.get('SETTINGS_POOL_SIZE', 250)
    env.command_timeout = config.get('SETTINGS_SSH_COMMAND_TIMEOUT', 60)
    env.disable_known_hosts = config.get('SETTINGS_DISABLE_KNOWN_HOSTS', True)

    if config['SETTINGS_FABRIC_FILE_PATH'] not in sys.path:
        sys.path.append(config['SETTINGS_FABRIC_FILE_PATH'])

    fab_task_list = get_fab_tasks(config['SETTINGS_FABRIC_FILE_PATH'])

    _type = operation.get('OPT_OPERATION_TYPE', '')

    if _type == u'ssh_status_detecting':
        ssh_status_detecting(operation, config)

    elif _type == u'ping_status_detecting':
        ping_status_detecting(operation, config)

    elif _type == u'custom_script_execute':
        custom_script_execute(operation, config)

    #elif _type == u'predefined_fabfile_execute':
    #    predefined_fabfile_execute(operation, config, fab_task_list)

    elif _type == u'remote_power_control':
        remote_power_control(operation, config)

    else:
        logger.error(u'Error operation type. ID is %s' % operation['OPT_ID'])