#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import task, run

@task
def get_system_hostname():
    """ 获取操作系统时区设置"""
    run('date -R')