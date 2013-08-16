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
from flask import Blueprint, current_app, request, jsonify, json, abort

from frontend.extensions.database import db
from frontend.extensions.weixin import return_message, signature_verification
from frontend.models.operation import OperationDb

api = Blueprint('api', __name__, url_prefix='/api')

weichat_help_message = u'''Bongos Project的微信接口支持如下功能:
1. SSH状态测试
    ssh list /获取SSH权限列表/
    ssh Ssh_ID@8.8.8.8,114.114.114.114
2. PING联通性测试
    ping 8.8.8.8,114.114.114.114
4. FABFILE远程操作
    ssh list
    fab list /获取FABFILE列表/
    fab Ssh_ID@8.8.8.8,114.114.114.114 Fabfile_ID
3. IPMI电源管理
    ipmi list /获取IPMI权限列表/
    ipmi Ipmi_ID@8.8.8.8,114.114.114.114 reset/shutdown/poweron/poweroff'''

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

                if content == 'h' or content == 'help':
                    message = weichat_help_message

                elif content == 'get_openid':
                    message = sender
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