#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import task, run

@task
def get_system_kernel():
    """ Connect to a remote system to gather its kernel version. """
    run('uname -r')