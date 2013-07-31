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
from jinja2 import Template
from fabric.api import env, run, hide, execute
from paramiko.ssh_exception import SSHException
from fabric.exceptions import NetworkError, CommandTimeout

from backend.extensions.logger import logger
from backend.extensions.utility import generate_private_path, analysis_script_output


def final_custom_execute(USERNAME, PASSWORD, PORT, PRIVATE_KEY, SCRIPT_TEMPLATE, TEMPLATE_VARS):

    """
    :Return Code Description:

        0: PING SUCCESS(SUCCESS)
        1: PING FAIL(TIMEOUT)

        0: SSH SUCCESS(SUCCESS)
        1: SSH FAIL(TIMEOUT, RESET, NO_ROUTE)
        2: SSH AUTHENTICATE FAIL(验证错误, 密钥格式错误, 密钥无法找到)
        3: COMMAND EXECUTE TIMEOUT(脚本执行超时)
        4: COMMAND EXECUTE FAIL(脚本中途失败)

        10: NETWORK ERROR(ADDRESS ERROR)

        20: OTHER ERROR
        100: DEFAULT

        SSH认证是先看private_key，后看password.

    """

    env.user = USERNAME
    env.password = PASSWORD
    env.port = PORT
    env.key_filename = PRIVATE_KEY

    template = Template(SCRIPT_TEMPLATE)
    script = template.render(TEMPLATE_VARS.get(env.host, dict()))

    # TODO: 统计其它异常情况

    try:
        data = run(script, shell=True, quiet=True)
        if data.return_code == 0:
            output = dict(code=0,
                          error_message=data.stderr,
                          message=analysis_script_output(data.stdout))
        else:
            output = dict(code=data.return_code,
                          error_message=data.stderr,
                          message=data.stdout)

    # SystemExit 认证失败
    except SystemExit:
        output = dict(code=2, error_message='Ssh Authentication Failed', message='')

    # 远程命令执行时间超过`env.command_timeout`时触发
    except CommandTimeout:
        output = dict(code=3, error_message='Remote Command Execute Timeout', message='')

    # 通过设定`env.disable_known_hosts = True`可以避归此问题，但在异常处理上依然保留此逻辑。
    except SSHException, e:
        if 'Invalid key' in e.__str__():
            output = dict(code=2, error_message='User’s Known-Hosts Check Failed', message='')
        else:
            output = dict(code=20, error_message='SSHException Exception: %s' % e, message='')

    # 匹配错误的密钥路径
    except IOError, e:
        if 'No such file or directory' in e.__str__():
            output = dict(code=2, error_message='Ssh Private Key Not Found', message='')
        else:
            output = dict(code=20, error_message='IOError Exception: %s' % e, message='')

    except NetworkError, e:
        # 匹配SSH连接超时
        if 'Timed out trying to connect to' in e.__str__() or 'Low level socket error connecting' in e.__str__():
            output = dict(code=1, error_message='Ssh Connection Timeout', message='')
        elif 'Name lookup failed for' in e.__str__():
            output = dict(code=10, error_message='Incorrect Node Address', message='')
        else:
            output = dict(code=20, error_message='NetworkError Exception: %s' % e, message='')

    except Exception, e:
        if 'Private key file is encrypted' in e.__str__():
            output = dict(code=2, error_message='Private key file is encrypted', message='')
        else:
            output = dict(code=20, error_message='Base Exception: %s' % e, message='')

    return output


def custom_script_execute(operation, config):
    """
    :Return Code Description:

        0: 执行中
        1: 已完成
        2: 内部错误

    """

    id = operation.get('OPT_ID', 0)
    update_api_url = '%s/operation' % config.get('SETTINGS_API_BASIC_URL', 'http://localhost/api')

    with hide('everything'):

        result = execute(final_custom_execute,
                         operation.get('SSH_USERNAME', 'root'),
                         operation.get('SSH_PASSWORD', 'password'),
                         operation.get('SSH_PORT', 22),
                         generate_private_path(operation.get('SSH_PRIVATE_KEY', 'default.key')),
                         operation.get('OPT_SCRIPT_TEMPLATE', 'uptime'),
                         json.loads(operation.get('OPT_TEMPLATE_VARS', dict())),
                         hosts=operation.get('OPT_SERVER_LIST', '').split())

    data = json.dumps(dict(id=id, status=1, result=result),  ensure_ascii=False)

    response = requests.put(update_api_url, data=data, headers={'content-type': 'application/json'})

    if response.status_code != requests.codes.ok:
        message = response.json.get('message', 'unknown errors')
        logger.error(u'UPDATE OPERATION FAILS| Operation ID is %s, Message is %s' % (id, message))


def final_predefined_execute(USERNAME, PASSWORD, PORT, PRIVATE_KEY, SCRIPT_TEMPLATE, TEMPLATE_VARS):
    """
    :Return Code Description:

        0: PING SUCCESS(SUCCESS)
        1: PING FAIL(TIMEOUT)

        0: SSH SUCCESS(SUCCESS)
        1: SSH FAIL(TIMEOUT, RESET, NO_ROUTE)
        2: SSH AUTHENTICATE FAIL(验证错误, 密钥格式错误, 密钥无法找到)
        3: COMMAND EXECUTE TIMEOUT(脚本执行超时)
        4: COMMAND EXECUTE FAIL(脚本中途失败)

        10: NETWORK ERROR(ADDRESS ERROR)

        20: OTHER ERROR
        100: DEFAULT

        SSH认证是先看private_key，后看password.

    """

    env.user = USERNAME
    env.password = PASSWORD
    env.port = PORT
    env.key_filename = PRIVATE_KEY

    template = Template(SCRIPT_TEMPLATE)
    script = template.render(TEMPLATE_VARS.get(env.host, dict()))

    # TODO: 统计其它异常情况

    try:
        data = run(script, shell=True, quiet=True)
        if data.return_code == 0:
            output = dict(code=0,
                          error_message=data.stderr,
                          message=analysis_script_output(data.stdout))
        else:
            output = dict(code=data.return_code,
                          error_message=data.stderr,
                          message=data.stdout)

    # SystemExit 认证失败
    except SystemExit:
        output = dict(code=2, error_message='Ssh Authentication Failed', message='')

    # 远程命令执行时间超过`env.command_timeout`时触发
    except CommandTimeout:
        output = dict(code=3, error_message='Remote Command Execute Timeout', message='')

    # 通过设定`env.disable_known_hosts = True`可以避归此问题，但在异常处理上依然保留此逻辑。
    except SSHException, e:
        if 'Invalid key' in e.__str__():
            output = dict(code=2, error_message='User’s Known-Hosts Check Failed', message='')
        else:
            output = dict(code=20, error_message='SSHException Exception: %s' % e, message='')

    # 匹配错误的密钥路径
    except IOError, e:
        if 'No such file or directory' in e.__str__():
            output = dict(code=2, error_message='Ssh Private Key Not Found', message='')
        else:
            output = dict(code=20, error_message='IOError Exception: %s' % e, message='')

    except NetworkError, e:
        # 匹配SSH连接超时
        if 'Timed out trying to connect to' in e.__str__() or 'Low level socket error connecting' in e.__str__():
            output = dict(code=1, error_message='Ssh Connection Timeout', message='')
        elif 'Name lookup failed for' in e.__str__():
            output = dict(code=10, error_message='Incorrect Node Address', message='')
        else:
            output = dict(code=20, error_message='NetworkError Exception: %s' % e, message='')

    except Exception, e:
        if 'Private key file is encrypted' in e.__str__():
            output = dict(code=2, error_message='Private key file is encrypted', message='')
        else:
            output = dict(code=20, error_message='Base Exception: %s' % e, message='')

    return output


def predefined_script_execute(operation, config):
    """
    :Return:

        0: 执行中
        1: 已完成
        2: 内部错误

    """

    id = operation.get('OPT_ID', 0)
    update_api_url = '%s/operation' % config.get('SETTINGS_API_BASIC_URL', 'http://localhost/api')

    with hide('everything'):

        result = execute(final_predefined_execute,
                         operation.get('SSH_USERNAME', 'root'),
                         operation.get('SSH_PASSWORD', 'password'),
                         operation.get('SSH_PORT', 22),
                         generate_private_path(operation.get('SSH_PRIVATE_KEY', 'default.key')),
                         operation.get('SCRIPT_SCRIPT', 'uptime'),
                         json.loads(operation.get('OPT_TEMPLATE_VARS', dict())),
                         hosts=operation.get('OPT_SERVER_LIST', '').split())

    data = json.dumps(dict(id=id, status=1, result=result),  ensure_ascii=False)

    response = requests.put(update_api_url, data=data, headers={'content-type': 'application/json'})

    if response.status_code != requests.codes.ok:
        message = response.json.get('message', 'unknown errors')
        logger.error(u'UPDATE OPERATION FAILS| Operation ID is %s, Message is %s' % (id, message))