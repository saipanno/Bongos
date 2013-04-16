#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/04/16.
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


import json
from fabric.api import env, run, hide, execute
from fabric.exceptions import NetworkError

from web import db

from web.models.dashboard import SshConfig


def ssh_connectivity_checking(operate):
    """
    :Return:

         0: success
         1: fail
        -1: auth error
        -2: network error
        st: other error
    """

    env.user = operate.get('username', None)
    env.port = operate.get('port', None)
    env.password = operate.get('password', None)
    env.key_filename = operate.get('key_filename', None)

    try:
        output = run('uptime', shell=True, quiet=True)
        connectivity = output.return_code
    except SystemExit:
        connectivity = -1
    except NetworkError:
        connectivity = -2
    except Exception, e:
        connectivity = 'error: %s' % e

    return connectivity


def execute_ssh_task(task):

    ssh_config_id = task.ssh_config
    try:
        ssh_config = SshConfig.query.filter_by(id=int(ssh_config_id)).first()
    except Exception, e:
        do = e
        ssh_config = None

        task.status = 2

    if ssh_config is not None:
        env.user = ssh_config.username
        env.port = ssh_config.port
        env.password = ssh_config.password
        env.key_filename = ssh_config.key_filename

        with hide('stdout', 'stderr', 'running', 'aborts'):

            do = execute(ssh_connectivity_checking,
                         task,
                         hosts=task.server_list.split())

        task.status = 1
    else:
        task.status = 2
        do = 'error ssh config.'

    task.result = json.dumps(do, ensure_ascii=False)

    db.session.commit()
