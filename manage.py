#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

from flask.ext.script import Manager

from application import app
app.config.from_object('config')

manager = Manager(app)
manager.add_option("-c", "--config", dest="config", required=False)


if __name__ == '__main__':
    manager.run()