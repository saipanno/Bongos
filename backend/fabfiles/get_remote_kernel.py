#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import task, run

@task
def get_remote_kernel(**kwargs):
    output = run('uname -r')
    return dict(code=output.return_code, error_message=output.stderr, message=output.stdout)