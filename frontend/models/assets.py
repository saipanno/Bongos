#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/08/04.
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


from frontend.models.account import Group

from frontend.extensions.database import db


ServerGroup = db.Table('rs_server_group',
                       db.Column('server_id', db.Integer, db.ForeignKey('servers.id', ondelete='CASCADE')),
                       db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE')))


class Server(db.Model):

    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50))
    assets_number = db.Column(db.String(50))
    groups = db.relationship('Group', secondary=ServerGroup, backref=db.backref('servers', lazy='dynamic'),
                             passive_deletes=True)
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
        self.set_groups(group)
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

    def set_groups(self, groups):
        for group in self.groups:
            self.groups.remove(group)
        if groups:
            for group in groups:
                self.append_group(group)

    def append_group(self, group):
        if group and isinstance(group, Group):
            # reload tag by id to void error that <object xxx is already attached in session>
            renew_group = Group.query.get(group.id)
            self.groups.append(renew_group)

    def delete_group(self, group):
        if group and isinstance(group, Group):
            # reload tag by id to void error that <object xxx is already attached in session>
            renew_group = Group.query.get(group.id)
            self.groups.remove(renew_group)


class IDC(db.Model):

    __tablename__ = 'datacenters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(100))
    operators = db.Column(db.String(50))
    address = db.Column(db.Text)

    def __init__(self, name, desc, operators, address):

        self.name = name
        self.desc = desc
        self.operators = operators
        self.address = address