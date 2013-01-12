#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multichecking,
#
#         socket或ping并发测试脚本 
#
#
#    Created by Ruoyan Wong on 2012/11/04.

import os
import time
import socket
import subprocess
from argparse import ArgumentParser
from multiprocessing import Pool, Manager


def running_command(command):
    try:
        subprocess.call('%s >> /dev/null 2>&1' % command, shell=True)
    except Exception:
        pass

def connectivity_checking(address, result, COUNT, TIMEOUT):
    command = 'ping -c%s -W%s %s >> /dev/null 2>&1' % (COUNT, TIMEOUT, address)
    try:
        connectivity = subprocess.call(command, shell=True)
    except Exception:
        connectivity = -1
    finally:
        result[address] = connectivity

def socket_checking(address, port, result, TIMEOUT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    status = 0
    try:
        s.connect((address, port))
    except socket.timeout:
        status = 1
    except Exception:
        status = -1
    finally:
        s.close()
        result[address] = status


if __name__ == '__main__':

    HOME = os.environ['HOME']

    parser = ArgumentParser()
    parser.add_argument('target', help='hostname or address file')
    parser.add_argument('-o', dest='operate', help='operate type.', choices=['ping', 'socket'], required=True)
    parser.add_argument('-d', dest='logdir',  help='syslog directory, (default: %(default)s)', default='%s/logging' % HOME)
    parser.add_argument('-r', dest='procs',   help='process number, (default: %(default)s)', default=250, type=int)
    parser.add_argument('-t', dest='timeout', help='script build-in timeout, (default: %(default)s)', default=10)
    config = vars(parser.parse_args())

    subdirectories = '%s/%s' % (config['logdir'], time.strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % subdirectories)
    running_command('mv -f %s/*.txt %s' % (config['logdir'], subdirectories))
    running_command('mv -f %s/*.stat %s' % (config['logdir'], subdirectories))

    manager = Manager()
    kitten = manager.dict()

    tasks = list()
    with open(config['target']) as f:
        for oneline in f:
            oneline = oneline.rsplit()[0]
            tasks.append(oneline.split(','))

    pool = Pool(processes=config['procs'])

    jobs = list()
    if config['operate'] == 'ping':
        for task in tasks:
            # task = [address]
            pool.apply_async(connectivity_checking, (task[0], kitten, 5, config['timeout']))
    elif config['operate'] == 'socket':
        for task in tasks:
            # task = [address, port]
            pool.apply_async(socket_checking, (task[0], int(task[1]), kitten, config['timeout']))

    pool.close()
    pool.join()

    result_log_file = '%s/checking.txt' % config['logdir'] 
    with open(result_log_file, 'w') as f:
        for address in kitten.keys():
            f.write('%s : %s\n' % (address, kitten[address]))
