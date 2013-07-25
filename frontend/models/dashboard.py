#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/21.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from frontend.extensions.database import db


class SshConfig(db.Model):

    __tablename__ = 'ssh_config_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    port = db.Column(db.Integer)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    private_key = db.Column(db.String(50))

    def __init__(self, name, desc, port, username, password, private_key=None):
        self.name = name
        self.desc = desc
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key


class PreDefinedScript(db.Model):

    __tablename__ = 'predefined_script_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    script = db.Column(db.Text)
    author = db.Column(db.Integer)

    def __init__(self, name, desc, script, author):
        self.name = name
        self.desc = desc
        self.script = script
        self.author = author


class Server(db.Model):

    __tablename__ = 'server_lists'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50))
    assets_number = db.Column(db.String(50))
    groups = db.Column(db.String(50))
    desc = db.Column(db.Text)
    ext_address = db.Column(db.String(250), unique=True)
    int_address = db.Column(db.String(250), unique=True)
    ipmi_address = db.Column(db.String(250), unique=True)
    other_address = db.Column(db.String(250))
    idc = db.Column(db.Integer)
    rack = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    model = db.Column(db.String(250))
    cpu_info = db.Column(db.Text)
    disk_info = db.Column(db.Text)
    memory_info = db.Column(db.Text)

    def __init__(self, serial_number, assets_number, group, desc, ext_address, int_address, ipmi_address, other_address,
                 idc, rack, manufacturer, model, cpu_info, disk_info, memory_info):
        self.serial_number = serial_number
        self.assets_number = assets_number
        self.group = group
        self.desc = desc
        self.ext_address = ext_address
        self.int_address = int_address
        self.ipmi_address = ipmi_address
        self.other_address = other_address
        self.idc = idc
        self.rack = rack
        self.manufacturer = manufacturer
        self.model = model
        self.cpu_info = cpu_info
        self.disk_info = disk_info
        self.memory_info = memory_info


class Permission(db.Model):

    __tablename__ = 'access_control_lists'

    id = db.Column(db.Integer, primary_key=True)
    function = db.Column(db.String(250), unique=True)
    access_rules = db.Column(db.Text)

    def __init__(self, function, access_rules):

        self.function = function
        self.access_rules = access_rules


class IDC(db.Model):

    __tablename__ = 'idc_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(50))
    operators = db.Column(db.String(50))
    address = db.Column(db.Text)

    def __init__(self, name, desc, operators, address):

        self.name = name
        self.desc = desc
        self.operators = operators
        self.address = address
