#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/04/24.
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
import os
from fabric.api import run, local
from paramiko.ssh_exception import SSHException
from fabric.exceptions import NetworkError, CommandTimeout

import settings


def generate_private_path(filename):

    if filename is not u'':
        return os.path.join(settings.PRIVATE_KEY_PATH, filename)
    else:
        return None


def analysis_script_output(output):

    # \S 匹配所有非空字符
    # +? 匹配前面正则一次或多次，非贪婪模式
    regexp = 'BD:\S+?:EOF'

    fruit = re.findall(regexp, output)

    # 字符串掐头去尾操作，删除BD:和:EOF
    return ' '.join(fruit[3:][:-4])


def generate_ipmi_address(address):

    fruit = address.split('.')

    return '%s.%s.%s' % (settings.IPMI_NETWORK, fruit[2], fruit[3])


def run_with_exceptions(command, **kwargs):

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

    # TODO: 统计其它异常情况

    try:
        data = run(command, **kwargs)
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


def local_with_exceptions(command, **kwargs):

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

    # TODO: 统计其它异常情况

    try:
        data = local(command, **kwargs)
        if data.return_code == 0 or data.return_code == 1:
            output = dict(code=data.return_code, error_message='', message='')
        elif data.return_code == 2 and 'unknown host' in data.stderr:
            output = dict(code=10, error_message='Incorrect Node Address', message='')
        else:
            output = dict(code=data.return_code, error_message=data.stderr, message=data.stdout)

    except Exception, e:
        output = dict(code=20, error_message='Base Exception: %s' % e, message='')

    return output