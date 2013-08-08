#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/07/29.
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
from backend.libs.basic_local_runner import base_local_runner


def ping_connectivity_detecting(operation, config):
    """
    :Return:

        0: 执行中
        1: 已完成
        2: 内部错误

    """

    ID = operation.get('OPT_ID', 0)
    API_URL = '%s/operation' % config.get('SETTINGS_API_BASIC_URL', None)

    COMMAND = 'ping -c%s -W%s {{ address }}' % \
              (config.get('SETTINGS_PING_COUNT', 4), config.get('SETTINGS_PING_TIMEOUT', 5))

    if API_URL is not None:
        with hide('everything'):
            result = execute(base_local_runner, COMMAND,
                             hosts=operation.get('OPT_SERVER_LIST', '').split())

        data = json.dumps(dict(id=ID, status=1, result=result),  ensure_ascii=False)

        response = requests.put(API_URL, data=data, headers={'content-type': 'application/json'})

        if response.status_code != requests.codes.ok:
            message = response.json.get('message', 'unknown errors')
            logger.error(u'UPDATE OPERATION FAILS|Operation ID is %s, Message is %s' % (ID, message))

    else:
        logger.error(u'CONFIG FAILS|Message is can\'t get API url from config')