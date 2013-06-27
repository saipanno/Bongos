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


import re
import json
from fabric.api import env, run, hide, execute
from fabric.exceptions import NetworkError

from web import db

from web.dashboard.models import SshConfig


def create_script_from_template(template_script, template_vars, address):

    if len(template_vars) > 0:

        try:
            for key, value in template_vars[address].items():
                template_script = re.sub('{%s}' % key, value, template_script)
        except Exception, e:
            template_script = None

    return template_script


def final_custom_execute(user, port, password, key_filename, template_script, template_vars):
    """
    :Return:

         0: success
         1: fail
         2: auth error
         3: network error
         5: other error
    """

    env.user = user
    env.port = port
    env.password = password
    env.key_filename = key_filename

    script = create_script_from_template(template_script, template_vars, env.host)

    if script is not None:

        try:
            output = run(script, shell=True, quiet=True)
            connectivity = output.return_code
        except SystemExit:
            connectivity = 2
        except NetworkError:
            connectivity = 3
        except Exception, e:
            connectivity = 5

    else:

        connectivity = 6

    return connectivity


def custom_script_execute(config, task):

    # 修改任务状态，标记为操作中。
    task.status = 5
    db.session.commit()

    try:
        ssh_config_id = task.ssh_config
        ssh_config = SshConfig.query.filter_by(id=int(ssh_config_id)).first()
    except Exception, e:
        task.status = 2
        task.result = u'%s' % e
        ssh_config = None

    try:
        template_script = task.template_script
    except Exception, e:
        task.status = 2
        task.result = u'%s' % e
        template_script = None

    try:
        template_vars = json.loads(task.template_vars)
    except Exception, e:
        task.status = 2
        task.result = u'%s' % e
        template_vars = None

    if ssh_config is not None and template_script is not None and template_vars is not None:

        with hide('everything'):

            do = execute(final_custom_execute,
                         ssh_config.username,
                         ssh_config.port,
                         ssh_config.password,
                         ssh_config.key_filename,
                         template_script,
                         template_vars,
                         hosts=task.server_list.split())

        task.status = 1
        task.result = json.dumps(do, ensure_ascii=False)

    db.session.commit()
