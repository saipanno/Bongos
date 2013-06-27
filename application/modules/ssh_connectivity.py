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
from fabric.api import env, run, hide, execute
from fabric.exceptions import NetworkError, CommandTimeout
from sqlalchemy.exc import SQLAlchemyError

from web import db
from application.extensions import logger

from web.dashboard.models import SshConfig


def final_ssh_checking(user, port, password, key_filename, operate):
    """
    :Return:

         0: success
         1: fail
         2: auth error
         3: network error
         4: command timeout
         5: other error
    """

    env.user = user
    env.port = port
    env.password = password
    env.key_filename = key_filename

    try:
        output = run('ls', shell=True, quiet=True)
        connectivity = output.return_code
    except SystemExit:
        connectivity = 2
    except NetworkError:
        connectivity = 3
    except CommandTimeout:
        connectivity = 4
    except Exception, e:
        logger.error('TYPE:%s, ID:%s, MESSAGE: %s' % (operate.operate_type, operate.id, e))
        connectivity = 5

    return connectivity


def ssh_connectivity_checking(config, operate):

    logger.info('TYPE:%s, ID:%s, HOSTS: %s' % (operate.operate_type, operate.id, operate.server_list))

    # 修改任务状态，标记为操作中。
    operate.status = 5
    db.session.commit()

    try:
        ssh_config_id = operate.ssh_config
        ssh_config = SshConfig.query.filter_by(id=int(ssh_config_id)).first()
    except SQLAlchemyError, e:
        logger.error('TYPE:%s, ID:%s, MESSAGE: %s' % (operate.operate_type, operate.id, e))
        operate.status = 2
        operate.result = 'internal database error'
        ssh_config = None
    except Exception, e:
        logger.error('TYPE:%s, ID:%s, MESSAGE: %s' % (operate.operate_type, operate.id, e))
        operate.status = 2
        operate.result = 'error ssh configuration'
        ssh_config = None

    with hide('everything'):

        do = execute(final_ssh_checking,
                     ssh_config.username,
                     ssh_config.port,
                     ssh_config.password,
                     ssh_config.key_filename,
                     operate,
                     hosts=operate.server_list.split())

    operate.status = 1
    operate.result = json.dumps(do, ensure_ascii=False)

    db.session.commit()

    logger.info('TYPE:%s, ID:%s, MESSAGE: %s' % (operate.operate_type, operate.id, 'Operate Finished.'))
