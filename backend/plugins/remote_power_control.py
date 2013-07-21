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


import re
import json
from fabric.api import env, hide, show, local, execute

from backend.extensions.database import db
from backend.extensions.logger import logger
from backend.extensions.utility import generate_ipmi_address


def final_power_management(ipmi_user, ipmi_password, operate, spec=None):
    """
    :Return:

        default return: dict(code=100, msg='')

        0: PING SUCCESS(可联通)
        1: PING FAIL(超时)

        0: SSH SUCCESS(成功)
        1: SSH FAIL(超时, RESET, NO_ROUTE)
        2: SSH AUTHENTICATE FAIL(验证错误, 密钥格式错误, 密钥无法找到)
        3: COMMAND EXECUTE TIMEOUT(脚本执行超时)
        4: COMMAND FAIL(ERROR OUTPUT FORMAT)

        10: NETWORK ERROR(IP无法解析)

        20: OTHER ERROR
        100: DEFAULT

    """

    fruit = dict(code=100, msg='')

    ipmi_address = generate_ipmi_address(env.host)

    ipmitool_power_parameters = {0: 'reset', 1: 'off', 2: 'on', 3: 'status'}

    specifies = '-I lanplus' if spec else ''
    command = 'ipmitool %s -H %s -U %s -P %s chassis power %s' % (specifies, ipmi_address, ipmi_user, ipmi_password,
                                                                  ipmitool_power_parameters.get(operate, 'status'))

    try:
        output = local(command, capture=True)
        if output.return_code == 0:
            fruit['code'] = 0
            fruit['msg'] = 'Successful! %s' % output.stdout
        elif output.return_code == 1:
            fruit['code'] = 1
            if re.match(u'Activate Session command failed', output.stderr):
                fruit['error'] = 'IPMI connection failed'
                logger.warning(u'IPMI Connection Failed. ADDRESS: %s USER: %s, PASSWORD: %s' %
                               (ipmi_address, ipmi_user, ipmi_password))
            elif re.match(u'Invalid chassis power command', output.stderr):
                fruit['error'] = 'Wrong type of power operate'
            else:
                fruit['error'] = output.stderr
        else:
            fruit['code'] = 20
            fruit['error'] = output.stderr

    except Exception, e:
        fruit['code'] = 20
        fruit['error'] = '%s' % e

        logger.warning(u'UNKNOWN FAILS. MESSAGE: IPMI exec %s fails, except status is %s, except message is %s' %
                       (env.host, fruit['code'], fruit['error']))

    finally:
        return fruit


def exec_power_management(config, operation):
    """
    :Return:

        0: 队列中
        1: 已完成
        2: 内部错误
        5: 执行中

    """

    # 修改任务状态，标记为操作中。
    operation.status = 5
    db.commit()

    if operation.script_template == u'0':
        operate = u'reset'
    elif operation.script_template == u'1':
        operate = u'off'
    elif operation.script_template == u'2':
        operate = u'on'
    else:
        operate = u'status'

    with hide('everything'):

        do_exec = execute(final_power_management, config.get('IPMI_USER', 'root'),
                          config.get('IPMI_PASSWORD', 'calvin'), operate,
                          hosts=operation.server_list.split())

    operation.status = 1

    try:
        operation.result = json.dumps(do_exec, ensure_ascii=False)
    except Exception, e:
        operation.status = 2
        message = 'Integrate data error. %s' % e
        logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                     (operation.id, operation.operation_type, operation.status, message))

    db.commit()