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
from fabric.api import env, run, local, hide, show, execute
from fabric.exceptions import NetworkError, CommandTimeout

from backend.models import SshConfig
from backend.extensions.database import db
from backend.extensions.logger import logger
from backend.extensions.utility import generate_private_path, analysis_script_output


def final_ping_detecting(COUNT, TIMEOUT):
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

    command = 'ping -c%s -W%s %s' % (COUNT, TIMEOUT, env.host)

    try:
        output = local(command, capture=True)
        if output.return_code == 0:
            fruit['code'] = 0
        elif output.return_code == 1:
            fruit['code'] = 1
        elif output.return_code == 2 and 'unknown host' in output.stderr:
            fruit['code'] = 10
            fruit['msg'] = 'Network address error'

    except Exception, e:
        fruit['code'] = 20
        fruit['msg'] = '%s' % e

        logger.warning(u'UNKNOWN FAILS| Ping %s fails, Status is %s, Message is %s' %
                       (env.host, fruit['code'], fruit['msg']))

    finally:
        return fruit


def ping_status_detecting(operation=None, config=None):
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

    with hide('everything'):

        do_exec = execute(final_ping_detecting, config.get('PING_COUNT', 4), config.get('PING_TIMEOUT', 5),
                          hosts=operation.server_list.split())

    operation.status = 1

    try:
        operation.result = json.dumps(do_exec, ensure_ascii=False)
    except Exception, e:
        operation.status = 2
        logger.error(u'INTERNAL FAILS| Operation ID is %s, Operation status is %s, Message is %s' %
                     (operation.id, operation.status, e))

    db.commit()


def final_ssh_detecting(user, port, password, private_key):
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

        NetworkError = ["ssh.BadHostKeyException", "socket.gaierror", "socket.error", "ssh.AuthenticationException", "ssh.PasswordRequiredException", "ssh.SSHException"]
        CommandTimeout = ["socket.timeout"]

        SSH认证是先看private_key，后看password.

    """

    env.user = user
    env.port = port
    env.password = password
    if private_key is not None:
        env.key_filename = private_key

    fruit = dict(code=100, msg='')

    try:
        output = run('uptime', shell=True, quiet=True)

        if output.return_code == 0:
            fruit['code'] = 0
            fruit['msg'] = analysis_script_output(output.stdout)
        else:
            fruit['code'] = 20
            # SSH联通性测试，不再保存命令输出。
            #fruit['msg'] = analysis_script_output(output.stdout)
            fruit['error'] = output.stderr

    # SystemExit 无异常说明字符串
    except SystemExit:
        fruit['code'] = 2
        fruit['error'] = 'Authentication failed'

    # CommandTimeout 无异常说明字符串
    except CommandTimeout:
        fruit['code'] = 3
        fruit['error'] = 'Script execute timeout'

    except NetworkError, e:
        if 'Timed out trying to connect to' in e.__str__() or 'Low level socket error connecting' in e.__str__():
            fruit['code'] = 1
            fruit['error'] = 'Connect timeout'

        elif 'Name lookup failed for' in e.__str__():
            fruit['code'] = 10
            fruit['error'] = 'Network address error'

        elif 'Authentication failed' in e.__str__():
            fruit['code'] = 2
            fruit['error'] = 'Authentication failed'

        # 通过DISABLE_KNOWN_HOSTS选项可以避归此问题，但在异常处理上依然保留此逻辑。
        elif 'Private key file is encrypted' in e.__str__():
            fruit['code'] = 2
            fruit['error'] = 'Private key file is encrypted'

        elif 'not match pre-existing key' in e.__str__():
            fruit['code'] = 2
            fruit['error'] = 'Host key verification failed'

        else:
            fruit['code'] = 20
            fruit['error'] = '%s' % e
            logger.warning(u'UNKNOWN FAILS. MESSAGE: Connect %s fails, except status is %s, except message is %s' %
                           (env.host, fruit['code'], fruit['error']))

    except Exception, e:
        if 'No such file or directory' in e:
            fruit['code'] = 2
            fruit['error'] = 'Can\'t find private key'
        else:
            fruit['code'] = 20
            fruit['error'] = '%s' % e

            logger.warning(u'UNKNOWN FAILS. MESSAGE: Connect %s fails, except status is %s, except message is %s' %
                           (env.host, fruit['code'], fruit['error']))

    finally:
        return fruit


def ssh_status_detecting(operation, config=None):
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

    try:
        ssh_config_id = operation.ssh_config
        ssh_config = db.query(SshConfig).filter_by(id=int(ssh_config_id)).first()
    except Exception, e:
        operation.status = 2
        message = 'Failed to get the ssh configuration. %s' % e
        logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                     (operation.id, operation.operation_type, operation.status, message))

    if operation.status != 2:

        with hide('everything'):

            do_exec = execute(final_ssh_checking,
                              ssh_config.username,
                              ssh_config.port,
                              ssh_config.password,
                              generate_private_path(ssh_config.private_key),
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