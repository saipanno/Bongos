#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    extensions.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).

from functools import wraps

from flask import flash, url_for, session, request, redirect

def login_required(f):
    """Redirect to login page if user not logged in"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Login required', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return wrapper