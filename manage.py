#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).


import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from website import Application

define("port", default=9000, help="default: 9000, required runserver", type=int)

def main():

    tornado.options.parse_command_line()

    print 'server started. port %s' % options.port
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()