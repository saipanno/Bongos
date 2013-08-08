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
import requests
from fabric.api import hide, execute

from backend.logger import logger
from backend.libs.utility import generate_ipmi_address
from backend.libs.basic_local_ipmi_runner import basic_local_ipmi_runner


def remote_control(operation, config):
    """
    :Return:

        0: 执行中
        1: 已完成
        2: 内部错误

    """

    ID = operation.get('OPT_ID', 0)
    API_URL = '%s/operation' % config.get('SETTINGS_API_BASIC_URL', None)

    ipmi_address_list = list()
    for address in operation.get('OPT_SERVER_LIST', '').split():
        ipmi_address_list.append(generate_ipmi_address(address))

    # TODO: 为部分机型增加IPMI_SPEC_TAG的支持，比如早起的HP服务器
    IPMI_SPEC_TAG = None

    specifies = '-I lanplus' if IPMI_SPEC_TAG else ''
    COMMAND = 'ipmitool %s -H {{ ipmi_address }} -U %s -P %s chassis power %s' % \
              (specifies, config.get('SETTINGS_IPMI_USER', 'root'),
               config.get('SETTINGS_IPMI_PASSWORD', 'password'), operation.get('OPT_SCRIPT_TEMPLATE', 'status'))

    if API_URL is not None:

        with hide('everything'):

            result = execute(basic_local_ipmi_runner, COMMAND,
                             stdout=True, stderr=True,
                             hosts=operation.get('OPT_SERVER_LIST', '').split())

        data = json.dumps(dict(id=ID, status=1, result=result),  ensure_ascii=False)

        response = requests.put(API_URL, data=data, headers={'content-type': 'application/json'})

        if response.status_code != requests.codes.ok:
            message = response.json.get('message', 'unknown errors')
            logger.error(u'UPDATE OPERATION FAILS| Operation ID is %s, Message is %s' % (ID, message))

    else:
        logger.error(u'CONFIG FAILS|Message is can\'t get API url from config')