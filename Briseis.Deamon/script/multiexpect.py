#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multiexpect.py,
#
#         expect并发执行脚本 
#
#
#    Created by Ruoyan Wong on 2012/11/06.

import sys
import os, re
import tempfile
import subprocess
from time import strftime
from multiprocessing import Pool
from argparse import ArgumentParser

def running_command(command):
    try:
        subprocess.call('%s >> /dev/null 2>&1' % command, shell=True)
    except Exception:
        print 'exec error:\n\t%s' % command

def create_script_from_template(template, info):

    if len(info) == 0:
        script = template
    elif len(info) > 0:
        command_list = list()
        s, script = tempfile.mkstemp() 

        # create script from template.
        with open(template, 'r') as f:
            for oneline in f:
                for key,value in info.items():
                    oneline = re.sub('{%s}' % key, value, oneline)
                command_list.append(oneline.strip())        
    
        with open(script, 'w') as f:
            for command in command_list:
                f.write('%s\n' % command)

    return script 

if __name__ == '__main__':

    HOME = os.environ['HOME']
    AUTO_EXPECT = '%s/bin/auto_login.expect' % HOME

    parser = ArgumentParser()
    parser.add_argument('target', help='hostname or address file')
    parser.add_argument('-o', dest='operate', help='operate type', choices=['run', 'test'], required=True)
    parser.add_argument('-u', dest='user',    help='user, (default: %(default)s)', default='root')
    parser.add_argument('-p', dest='port',    help='port, (default: %(default)s)', default=22)
    parser.add_argument('-d', dest='logdir',  help='syslog directory, (default: %(default)s)', default='%s/logging' % HOME)
    parser.add_argument('-i', dest='secret',  help='user identity file, (default: %(default)s)', default='%s/.ssh/ku_rsa' % HOME)
    parser.add_argument('-s', dest='shadow',  help='password file, (default: %(default)s)', default='%s/.ssh/ku_password' % HOME)
    parser.add_argument('-r', dest='procs',   help='process number, (default: %(default)s)', default=250, type=int)
    parser.add_argument('-t', dest='timeout', help='expect build-in timeout, (default: %(default)s)', default=45)
    script_run_group = parser.add_argument_group('OPTION: -o run')
    script_run_group.add_argument('-f', dest='script', help='script or template script file')
    script_run_group.add_argument('-v', dest='variable', help='variable for template file')
    config = vars(parser.parse_args())

    subdirectories = '%s/%s' % (config['logdir'], strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % subdirectories)
    running_command('mv -f %s/*.txt %s' % (config['logdir'], subdirectories))
    running_command('mv -f %s/*.stat %s' % (config['logdir'], subdirectories))

    hosts = list()
    with open(config['target']) as file:
        for oneline in file:
            hosts.append(oneline.rsplit()[0])

    pool = Pool(processes=config['procs'])

    COMMAND = 'expect %s' % AUTO_EXPECT
    for key,value in config.items():
        if key == 'operate' and value is not None:
            COMMAND = '%s o %s' % (COMMAND, value)
        elif key == 'user' and value is not None:
            COMMAND = '%s u %s' % (COMMAND, value)
        elif key == 'port' and value is not None:
            COMMAND = '%s p %s' % (COMMAND, value)
        elif key == 'secret' and value is not None:
            COMMAND = '%s i %s' % (COMMAND, value)
        elif key == 'shadow' and value is not None:
            COMMAND = '%s s %s' % (COMMAND, value)
        elif key == 'logdir' and value is not None:
            COMMAND = '%s d %s' % (COMMAND, value)
        elif key == 'timeout' and value is not None:
            COMMAND = '%s t %s' % (COMMAND, value)
   
    detail_dict = dict()
    if config['variable'] is not None and os.path.isfile(config['variable']):
        try:
            file = open(config['variable'])
            for oneline in file:
                detail_address = oneline.split("|")[0]
                detail_information = oneline.split("|")[1]
                detail_dict[detail_address] = dict() 
                for var in detail_information.split(","):
                    key = var.split("=")[0].strip()
                    value =var.split("=")[1].strip()
                    detail_dict[detail_address][key] = value
            file.close()
        except Exception, e:
            print 'get variable error: %s' % e
            sys.exit(1)

    for host in hosts:
        script = create_script_from_template(config['script'], detail_dict.get('host', dict()))
        pool.apply_async(running_command, ('%s f %s a %s' % (COMMAND, script, host), ))

    pool.close()
    pool.join()
