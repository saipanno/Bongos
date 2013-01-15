#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    helper.py, in Briseis.
#
#
#    Created at 2013/01/14. Ruoyan Wong(@saipanno).

def import_setting_from_config(obj):
    config = dict()
    for key in dir(obj):
        if key.isupper():
            config[key.lower()] = getattr(obj, key)
    return config