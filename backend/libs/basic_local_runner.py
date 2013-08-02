#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/08/01.
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


from jinja2 import Template
from fabric.api import env, local

from backend.libs.utility import analysis_script_output


def base_local_runner(SCRIPT_TEMPLATE, stdout=False, stderr=False, regex=False):
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

    template = Template(SCRIPT_TEMPLATE)
    script = template.render(dict(address=env.host))

    # TODO: 统计其它异常情况

    try:
        data = local(script, capture=True)
    except Exception, e:
        output = dict(code=20,
                      error_message='Base Exception: %s' % e if stderr else '',
                      message='')

    else:
        output = dict(code=data.return_code,
                      error_message=data.stderr if stderr else '',
                      message='' if not stdout else analysis_script_output(data.stdout) if regex else data.stdout)

    return output