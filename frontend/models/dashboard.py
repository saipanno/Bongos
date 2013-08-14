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


from frontend.models.account import Group
from frontend.extensions.database import db


SshConfigGroup = db.Table('rs_sshconfig_group',
                          db.Column('config_id', db.Integer, db.ForeignKey('ssh_configs.id', ondelete='CASCADE')),
                          db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE')))


class SshConfig(db.Model):

    __tablename__ = 'ssh_configs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    groups = db.relationship('Group', secondary=SshConfigGroup, backref=db.backref('ssh_configs', lazy='dynamic'),
                             passive_deletes=True)
    port = db.Column(db.Integer)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    private_key = db.Column(db.String(50))

    def __init__(self, name, desc, author_id, groups, port, username, password, private_key):
        self.name = name
        self.desc = desc
        self.author_id = author_id
        self.set_groups(groups)
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key

    def __repr__(self):
        return '<Ssh Config %s>' % self.name

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


IpmiConfigGroup = db.Table('rs_ipmiconfig_group',
                           db.Column('config_id', db.Integer, db.ForeignKey('ipmi_configs.id', ondelete='CASCADE')),
                           db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE')))


class IpmiConfig(db.Model):

    __tablename__ = 'ipmi_configs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    groups = db.relationship('Group', secondary=IpmiConfigGroup, backref=db.backref('ipmi_configs', lazy='dynamic'),
                             passive_deletes=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    interface = db.Column(db.Integer)

    def __init__(self, name, desc, author_id, groups, username, password, interface):
        self.name = name
        self.desc = desc
        self.author_id = author_id
        self.set_groups(groups)
        self.username = username
        self.password = password
        self.interface = interface

    def __repr__(self):
        return '<Ipmi Config %s>' % self.name

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


PermissionGroup = db.Table('rs_permission_group',
                           db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id', ondelete='CASCADE')),
                           db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE')))


class Permission(db.Model):

    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    handler = db.Column(db.String(250), unique=True)
    groups = db.relationship('Group', secondary=PermissionGroup, backref=db.backref('permissions', lazy='dynamic'),
                             passive_deletes=True)

    def __init__(self, handler, groups):

        self.handler = handler
        self.set_groups(groups)

    def __repr__(self):
        return '<Permission %s>' % self.name

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


FabFileGroup = db.Table('rs_fabfile_group',
                        db.Column('fabfile_id', db.Integer, db.ForeignKey('fabfiles.id', ondelete='CASCADE')),
                        db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE')))


class FabFile(db.Model):

    __tablename__ = 'fabfiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    groups = db.relationship('Group', secondary=FabFileGroup, backref=db.backref('fabfiles', lazy='dynamic'),
                             passive_deletes=True)

    def __init__(self, name, desc, author_id, groups):

        self.name = name
        self.desc = desc
        self.author_id = author_id
        self.set_groups(groups)

    def __repr__(self):
        return '<Fabfile %s>' % self.name

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