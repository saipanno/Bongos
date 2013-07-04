#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/04/17.
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
from jinja2 import Template
from fabric.api import env, run, hide, show, execute
from fabric.exceptions import NetworkError, CommandTimeout

from web import db

from web.dashboard.models import SshConfig, PreDefinedScript
from application.extensions import logger, get_private_key_path


def final_predefined_execute(user, port, password, private_key, script_template, template_vars):
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

    template = Template(script_template)
    script = template.render(template_vars.get(env.host, dict()))

    try:
        output = run(script, shell=True, quiet=True)
        if output.return_code == 0:
            fruit['code'] = 0
            fruit['msg'] = output.stdout
        else:
            fruit['code'] = 4
            fruit['msg'] = 'Success: %s, Error: %s' % (output.stdout, output.stderr)

    # SystemExit 无异常说明字符串
    except SystemExit:
        fruit['code'] = 2
        fruit['msg'] = 'Authentication failed'

    # CommandTimeout 无异常说明字符串
    except CommandTimeout:
        fruit['code'] = 3
        fruit['msg'] = 'Script execute timeout'

    except NetworkError, e:
        if 'Timed out trying to connect to' in e.__str__() or 'Low level socket error connecting' in e.__str__():
            fruit['code'] = 1
            fruit['msg'] = 'Connect timeout'

        elif 'Name lookup failed for' in e.__str__():
            fruit['code'] = 10
            fruit['msg'] = 'Network address error'

        elif 'Authentication failed' in e.__str__():
            fruit['code'] = 2
            fruit['msg'] = 'Authentication failed'

        # 通过DISABLE_KNOWN_HOSTS选项可以避归此问题，但在异常处理上依然保留此逻辑。
        elif 'Private key file is encrypted' in e.__str__():
            fruit['code'] = 2
            fruit['msg'] = 'Private key file is encrypted'

        elif 'not match pre-existing key' in e.__str__():
            fruit['code'] = 2
            fruit['msg'] = 'Host key verification failed'

        else:
            fruit['code'] = 20
            fruit['msg'] = '%s' % e
            logger.warning(u'UNKNOWN FAILS. MESSAGE: Connect %s fails, except status is %s, except message is %s' %
                           (env.host, fruit['code'], fruit['msg']))

    except Exception, e:
        if 'No such file or directory' in e:
            fruit['code'] = 2
            fruit['msg'] = 'Can\'t find private key'
        else:
            fruit['code'] = 20
            fruit['msg'] = '%s' % e

            logger.warning(u'UNKNOWN FAILS. MESSAGE: Connect %s fails, except status is %s, except message is %s' %
                           (env.host, fruit['code'], fruit['msg']))

    finally:
        return fruit


def predefined_script_execute(operate):
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

    try:
        ssh_config_id = operate.ssh_config
        ssh_config = SshConfig.query.filter_by(id=int(ssh_config_id)).first()
    except Exception, e:
        operate.status = 2
        message = 'Failed to get the ssh configuration. %s' % e
        logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                     (operate.id, operate.operate_type, operate.status, message))

    try:
        predefined_script_id = operate.script_template
        script_template = PreDefinedScript.query.filter_by(id=int(predefined_script_id)).first().script
    except Exception, e:
        operate.status = 2
        message = 'Failed to get the script template. %s' % e
        logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                     (operate.id, operate.operate_type, operate.status, message))

    try:
        template_vars = json.loads(operate.template_vars)
    except Exception, e:
        operate.status = 2
        message = 'Failed to load template vars. %s' % e
        logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                     (operate.id, operate.operate_type, operate.status, message))

    if operate.status != 2:

        with hide('everything'):

            do_exec = execute(final_predefined_execute,
                              ssh_config.username,
                              ssh_config.port,
                              ssh_config.password,
                              get_private_key_path(ssh_config.private_key),
                              script_template,
                              template_vars,
                              hosts=operate.server_list.split())

        operate.status = 1
        try:
            operate.result = json.dumps(do_exec, ensure_ascii=False)
        except Exception, e:
            operate.status = 2
            message = 'Integrate data error. %s' % e
            logger.error(u'ID:%s, TYPE:%s, STATUS: %s, MESSAGE: %s' %
                         (operate.id, operate.operate_type, operate.status, message))

    db.session.commit()