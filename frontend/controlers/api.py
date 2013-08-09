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


from flask import Blueprint, current_app, request, jsonify, json

from frontend.extensions.database import db
from frontend.models.operation import OperationDb

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/operation', methods=["PUT"])
def update_operation_status():

    if request.method == 'PUT':

        access_address = current_app.config.get('API_ACCESS_CLIENTS', '127.0.0.1')

        current_app.logger.info(str(request.json))

        if request.remote_addr in access_address:

            id = request.json.get('id', 0)
            status = request.json.get('status', 2)
            result = request.json.get('result', dict())

            operation = OperationDb.query.filter_by(id=id).first()

            if operation is not None:

                operation.status = status
                operation.result = json.dumps(result, ensure_ascii=False)

                db.session.commit()

                return jsonify({'status': 'success'})

            return jsonify({'status': 'error', 'message': 'Unknown operation number'})

        return jsonify({'status': 'error', 'message': 'Authentication permissions fails'})

    return jsonify({'status': 'error', 'message': 'Request method error'})