#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

#from flask.ext.script import Manager

from application import app

#manager = Manager(app)

def main():
    """启动本地进程."""
    app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    #manager.run()
    main()