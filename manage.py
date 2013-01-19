#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    manage.py, in Briseis.
#
#
#    Created at 2013/01/16. Ruoyan Wong(@saipanno).

from web import app

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])