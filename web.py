#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/16.
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


import argparse

from frontend.app import create_app


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='web app launcher.')
    parser.add_argument('-c', '--config', dest='config', default=None)

    args = vars(parser.parse_args())

    app = create_app(args['config'])
    app.run(host=app.config.get('HOST', '127.0.0.1'),
            port=app.config.get('PORT', 8080),
            debug=app.config.get('DEBUG', False))