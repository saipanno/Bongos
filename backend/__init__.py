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


from fabric.api import env

from backend.plugins.status_detecting import ssh_status_detecting
from backend.plugins.status_detecting import ping_status_detecting
from backend.plugins.remote_execute import custom_script_execute
from backend.plugins.remote_execute import predefined_script_execute
from backend.plugins.remote_control import remote_power_control


def task_runner(operation=None, config=None):

    env.parallel = True
    env.warn_only = True

    env.pool_size = config.get('POOL_SIZE', 250)
    env.timeout = config.get('SSH_TIMEOUT', 30)
    env.command_timeout = config.get('SSH_COMMAND_TIMEOUT', 60)
    env.disable_known_hosts = config.get('DISABLE_KNOWN_HOSTS', True)