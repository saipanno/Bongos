#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/07/26.
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


import xml.etree.cElementTree as et
from flask import Blueprint, current_app, request, jsonify, json, abort, url_for

from frontend.extensions.database import db
from frontend.extensions.weixin import return_message, signature_verification

from frontend.models.account import User
from frontend.models.operation import OperationDb

api = Blueprint('api', __name__, url_prefix='/api')

weichat_help_message = u'''Bongos Project的微信接口支持如下功能:
1. ssh  - ssh status detecting
   ssh list
   ssh SSH_ID@address1,address2

2. ping - ping connectivity detecting
   ping address1,address2

3. ipmi - remote power control
   ipmi list
   ipmi IPMI_ID@address1,address2 reset/poweron/poweroff

4. fab  - remote fabfile execute
   fab list
   ssh list
   fab SSH_ID@address1,address2 FAB_ID'''


@api.route('/weichat', methods=["GET", "POST"])
def check_signature_handler():

    if request.method == 'GET':

        if signature_verification(request.args, current_app.config.get('WEIXIN_TOKEN', '')):
            return request.args.get('echostr', None)

    if request.method == 'POST':

        if signature_verification(request.args, current_app.config.get('WEIXIN_TOKEN', '')):

            data = et.fromstring(request.data)
            if data.find("MsgType").text == 'text':
                receiver = data.find("ToUserName").text
                sender = data.find("FromUserName").text
                content = data.find("Content").text.lower()

                user = User.query.filter_by(weixin=sender).first()

                if user is None and content == 'bind':
                    message = u'访问如下链接进行帐号绑定:\n http://%s%s' % (
                        current_app.config.get('DOMAIN_NAME', 'localhost'),
                        url_for('account.binding_weixin_handler', weixin=sender))

                elif user is None:
                    message = u'当前帐号未绑定，请使用`bind`命令进行绑定操作.'

                elif content == 'h' or content == 'help':
                    message = weichat_help_message

                elif content == 'ssh list':
                    ssh_configs = list()
                    for group in user.groups:
                        for ssh_config in group.ssh_configs:
                            if not ssh_config in ssh_configs:
                                ssh_configs.append(ssh_config)
                    message = '\n'.join(['%s - %s' % (config.id, config.name) for config in ssh_configs])

                elif content == 'fab list':
                    fabfiles = list()
                    for group in user.groups:
                        for fabfile in group.ipmi_configs:
                            if not fabfile in fabfiles:
                                fabfiles.append(fabfile)
                    message = '\n'.join(['%s - %s' % (fabfile.id, fabfile.name) for fabfile in fabfiles])

                elif content == 'ipmi list':
                    ipmi_configs = list()
                    for group in user.groups:
                        for ipmi_config in group.ipmi_configs:
                            if not ipmi_config in ipmi_configs:
                                ipmi_configs.append(ipmi_config)
                    message = '\n'.join(['%s - %s' % (config.id, config.name) for config in ipmi_configs])

                else:
                    message = u'error request content'

                # variable exchange
                (receiver, sender) = (sender, receiver)

                return return_message(sender, receiver, message)

    abort(404)


@api.route('/operation/<int:id>', methods=["PUT"])
def update_operation_handler(id):

    if request.method == 'PUT':

        access_address = current_app.config.get('API_ACCESS_CLIENTS', '127.0.0.1')

        current_app.logger.info(str(request.json))

        if request.remote_addr in access_address:

            status = request.json.get('status', 2)
            result = request.json.get('result', dict())

            operation = OperationDb.query.get(id)

            if operation is not None:

                operation.status = status
                operation.result = json.dumps(result, ensure_ascii=False)

                db.session.commit()

                return jsonify({'status': 'success'})

    abort(404)