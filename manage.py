#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/12. Ruoyan Wong(@saipanno).

from application import app
app.config.from_object('config')


if __name__ == '__main__':
    app.run()