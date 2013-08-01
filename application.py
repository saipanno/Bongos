#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/02/22.
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


from backend.tasks import backend_runner


if __name__ == '__main__':


    backend_runner({'OPT_SERVER_LIST': u'8.8.8.8', 'OPT_ID': 72, 'OPT_RESULT': u'', 'OPT_SCRIPT_TEMPLATE': u'',
                    'OPT_OPERATION_TYPE': u'ping_status_detecting', 'OPT_SSH_CONFIG': 0, 'OPT_TEMPLATE_VARS': u'',
                    'OPT_DATETIME': u'2013-08-01 15:31', 'OPT_AUTHOR': u'1', 'OPT_STATUS': u'0'},
                   {'SETTINGS_APPLICATION_ROOT': None, 'SETTINGS_SSH_COMMAND_TIMEOUT': 120,
                    'SETTINGS_SESSION_COOKIE_NAME': 'session', 'SETTINGS_JSON_SORT_KEYS': True,
                    'SETTINGS_PRIVATE_KEY_PATH': '/Users/saipanno/Projects/Bongos/data/private_key',
                    'SETTINGS_LOGGING_LEVEL': 'WARNING', 'SETTINGS_JSONIFY_PRETTYPRINT_REGULAR': True,
                    'SETTINGS_SESSION_PROTECTION': 'strong', 'SETTINGS_SESSION_COOKIE_HTTPONLY': True,
                    'SETTINGS_MAX_CONTENT_LENGTH': None,
                    'SETTINGS_JSON_AS_ASCII': True, 'SETTINGS_SQLALCHEMY_BINDS': None,
                    'SETTINGS_SEND_FILE_MAX_AGE_DEFAULT': 43200,
                    'SETTINGS_LOGGING_FILENAME': '/Users/saipanno/Projects/Bongos/bongos.log',
                    'SETTINGS_PING_TIMEOUT': 5, 'SETTINGS_SSH_TIMEOUT': 30, 'SETTINGS_SQLALCHEMY_POOL_SIZE': None,
                    'SETTINGS_SESSION_COOKIE_SECURE': False, 'SETTINGS_PING_COUNT': 4, 'SETTINGS_PORT': 80,
                    'SETTINGS_SQLALCHEMY_DATABASE_URI': 'sqlite:////Users/saipanno/Projects/Bongos/sqlite.db',
                    'SETTINGS_SERVER_NAME': None,
                    'SETTINGS_SECRET_KEY': '\x17s\\\x8cY\x00X\xf3 .V\xfb\x01\xd0\xbb\x16Z`\xd84ZHk\xd7',
                    'SETTINGS_SQLALCHEMY_POOL_TIMEOUT': None, 'SETTINGS_SQLALCHEMY_POOL_RECYCLE': None,
                    'SETTINGS_SESSION_COOKIE_DOMAIN': None, 'SETTINGS_API_ACCESS_CLIENTS': ['127.0.0.1'],
                    'SETTINGS_IPMI_USER': 'root', 'SETTINGS_TRAP_HTTP_EXCEPTIONS': False,
                    'SETTINGS_PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SETTINGS_DEBUG': True,
                    'SETTINGS_IPMI_NETWORK': '192.168',
                    'SETTINGS_FABRIC_FILE_PATH': '/Users/saipanno/Projects/Bongos/backend/fabfile',
                    'SETTINGS_SQLALCHEMY_RECORD_QUERIES': None, 'SETTINGS_DISABLE_KNOWN_HOSTS': True,
                    'SETTINGS_SESSION_COOKIE_PATH': None, 'SETTINGS_TESTING': False,
                    'SETTINGS_PROPAGATE_EXCEPTIONS': None, 'SETTINGS_SQLALCHEMY_NATIVE_UNICODE': None,
                    'SETTINGS_POOL_SIZE': 250, 'SETTINGS_TRAP_BAD_REQUEST_ERRORS': False,
                    'SETTINGS_API_BASIC_URL': 'http://127.0.0.1/api', 'SETTINGS_LOGGER_NAME': 'frontend.app',
                    'SETTINGS_USE_X_SENDFILE': False, 'SETTINGS_IPMI_PASSWORD': 'hello-bongos',
                    'SETTINGS_SQLALCHEMY_ECHO': False, 'SETTINGS_HOST': '0.0.0.0',
                    'SETTINGS_PREFERRED_URL_SCHEME': 'http'})