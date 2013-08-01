#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import task, run

@task
def get_system_hostname():
    """ 获取操作系统主机名. Testing for edit."""
    run('hostname')