#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import task, run

@task
def get_system_uptime():
    """ 获取操作系统启动时间. """
    run('sleep 2')
    run('uptime')