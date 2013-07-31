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
import requests
from fabric.api import env, hide, local, execute

from backend.extensions.logger import logger
from backend.extensions.utility import generate_ipmi_address


def final_power_execute(IPMI_USER, IPMI_PASSWORD, IPMI_POWER_COMMAND, IPMI_SPEC_TAG=None):
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

    specifies = '-I lanplus' if IPMI_SPEC_TAG else ''
    command = 'ipmitool %s -H %s -U %s -P %s chassis power %s' % (specifies, ipmi_address,
                                                                  IPMI_USER, IPMI_PASSWORD, IPMI_POWER_COMMAND)

    try:
        output = local(command, capture=True)
        if output.return_code == 0:
            fruit['code'] = 0
            fruit['msg'] = output.stdout
        elif output.return_code == 1:
            fruit['code'] = 1
            if re.match(u'Activate Session command failed', output.stderr):
                fruit['error'] = 'IPMI Connection Failed'
                logger.warning(u'IPMI FAILS|Connection Failed. Address is %s User is %s, Password is %s' %
                               (ipmi_address, IPMI_USER, IPMI_PASSWORD))
            elif re.match(u'Invalid chassis power command', output.stderr):
                fruit['error'] = 'Invalid IPMI Power Command'
            else:
                fruit['error'] = output.stderr
        else:
            fruit['code'] = 20
            fruit['error'] = output.stderr

    except Exception, e:
        fruit['code'] = 20
        fruit['error'] = '%s' % e

        logger.warning(u'IPMI UNKNOWN FAILS|Message is %s' % fruit['error'])

    finally:
        return fruit


def power_supply_control(operation, config):
    """
    :Return:

        0: 执行中
        1: 已完成
        2: 内部错误

    """

    id = operation.get('OPT_ID', 0)
    update_api_url = '%s/operation' % config.get('SETTINGS_API_BASIC_URL', 'http://localhost/api')

    with hide('everything'):

        result = execute(final_power_execute,
                         config.get('SETTINGS_IPMI_USER', 'root'),
                         config.get('SETTINGS_IPMI_PASSWORD', 'password'),
                         operation.get('OPT_SCRIPT_TEMPLATE', 'status'),
                         hosts=operation.get('OPT_SERVER_LIST', '').split())

    data = json.dumps(dict(id=id, status=1, result=result),  ensure_ascii=False)

    response = requests.put(update_api_url, data=data, headers={'content-type': 'application/json'})

    if response.status_code != requests.codes.ok:
        message = response.json.get('message', 'unknown errors')
        logger.error(u'UPDATE OPERATION FAILS| Operation ID is %s, Message is %s' % (id, message))