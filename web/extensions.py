#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    extensions.py, in Briseis.
#
#
#    Created at 2013/01/21. Ruoyan Wong(@saipanno).


def format_server_group(servers):

    node = list()
    for server in servers.split('\n'):
        node.append(server)

    return node