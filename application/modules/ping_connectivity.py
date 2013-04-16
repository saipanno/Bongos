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
from fabric.api import env, hide, local, execute
from fabric.exceptions import NetworkError

from web import db


def ping_connectivity_checking(COUNT, TIMEOUT):
    """
    :Return:

         0: success
         1: fail
        -2: network error
        st: other error
    """

    command = 'ping -c%s -W%s %s >> /dev/null 2>&1' % (COUNT, TIMEOUT, env.host)

    try:
        output = local(command, capture=True)
        connectivity = output.return_code
    except NetworkError:
        connectivity = -2
    except Exception, e:
        connectivity = 'error: %s' % e

    return connectivity


def execute_ping_task(config, task):

    with hide('stdout', 'stderr', 'running', 'aborts'):

        do = execute(ping_connectivity_checking,
                     config.get('PING_COUNT', 5),
                     config.get('PING_TIMEOUT', 5),
                     hosts=task.server_list.split())

    task.status = 1
    task.result = json.dumps(do, ensure_ascii=False)

    db.session.commit()
