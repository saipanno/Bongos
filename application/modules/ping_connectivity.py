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

from web import db
from application.extensions import logger


def final_ping_checking(COUNT, TIMEOUT, operate):
    """
    :Return:

        default return: dict(code=20, msg='')

         0: PING SUCCESS(可联通)
         1: PING FAIL(超时)

         0: SSH SUCCESS(成功)
         1: SSH FAIL(超时, RESET, NO_ROUTE)
         2: SSH AUTHENTICATE FAIL(验证错误, 密钥格式错误, 密钥无法找到)
         3: COMMAND EXECUTE TIMEOUT(脚本执行超时)
         4: COMMAND FAIL(ERROR OUTPUT FORMAT)

         10: NETWORK ERROR(IP无法解析)

         20: OTHER ERROR

    """

    connectivity = dict(code=20, msg='')
    command = 'ping -c%s -W%s %s' % (COUNT, TIMEOUT, env.host)

    try:
        output = local(command, capture=True)
        if output.return_code == 0:
            connectivity['code'] = 0
        elif output.return_code == 1:
            connectivity['code'] = 1
        elif output.return_code == 2 and 'unknown host' in output.stderr:
            connectivity['code'] = 10
            connectivity['msg'] = 'Network address error'

    except Exception, e:
        connectivity['code'] = 20
        connectivity['msg'] = '%s' % e

        logger.warning(u'UNKNOWN FAILS. MESSAGE: Ping %s fails, except status is %s, except message is %s' %
                       (env.host, connectivity['code'], connectivity['msg']))

    finally:
        return connectivity


def ping_connectivity_checking(config, operate):
    """
    :Return:

        0: 队列中
        1: 已完成
        2: 内部错误
        5: 执行中

    """

    # 修改任务状态，标记为操作中。
    operate.status = 5
    db.session.commit()

    with hide('everything'):

        do_exec = execute(final_ping_checking, config.get('PING_COUNT', 4), config.get('PING_TIMEOUT', 5),
                          operate, hosts=operate.server_list.split())

    operate.status = 1

    try:
        operate.result = json.dumps(do_exec, ensure_ascii=False)
    except Exception, e:
        operate.status = 2
        message = 'Integrate data error. %s' % e
        logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                     (operate.id, operate.operate_type, operate.status, message))

    db.session.commit()