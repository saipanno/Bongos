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
from fabric.api import env, hide, show, local, execute
from fabric.exceptions import NetworkError, CommandTimeout

from web import db
from application.extensions import logger


def final_ping_checking(COUNT, TIMEOUT, operate):
    """
    :Return:

         0: success
         1: fail
         2: network error
         3: command timeout
         5: other error
    """

    command = 'ping -c%s -W%s %s >> /dev/null 2>&1' % (COUNT, TIMEOUT, env.host)

    try:
        result = local(command, capture=True)
        connectivity = result.return_code
    except NetworkError:
        connectivity = 2
    except CommandTimeout:
        connectivity = 3
    except Exception, e:
        logger.error('TYPE:%s, ID:%s, MESSAGE: %s' % (operate.operate_type, operate.id, e))
        connectivity = 5

    return connectivity


def ping_connectivity_checking(config, operate):

    logger.info('TYPE:%s, ID:%s, HOSTS: %s' % (operate.operate_type, operate.id, operate.server_list))

    # 修改任务状态，标记为操作中。
    operate.status = 5
    db.session.commit()

    with hide('everything'):

        do = execute(final_ping_checking,
                     config.get('PING_COUNT', 5),
                     config.get('PING_TIMEOUT', 5),
                     operate,
                     hosts=operate.server_list.split())

    operate.status = 1
    operate.result = json.dumps(do, ensure_ascii=False)

    db.session.commit()

    logger.info('TYPE:%s, ID:%s, MESSAGE: %s' % (operate.operate_type, operate.id, 'Operate Finished.'))
