#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/23.
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


from werkzeug.security import generate_password_hash, check_password_hash

from frontend.extensions.database import db


UserGroup = db.Table('rs_user_group',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
                     db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE')))


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    groups = db.relationship('Group', secondary=UserGroup, backref=db.backref('users', lazy='dynamic'),
                             passive_deletes=True)
    weixin = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    status = db.Column(db.Integer)
    operations = db.relationship('OperationDb', backref='author', lazy='dynamic',
                                 cascade='all,delete-orphan', passive_deletes=True)
    fabfiles = db.relationship('FabFile', backref='author', lazy='dynamic',
                               cascade='all,delete-orphan', passive_deletes=True)
    ssh_configs = db.relationship('SshConfig', backref='author', lazy='dynamic',
                                  cascade='all,delete-orphan', passive_deletes=True)
    ipmi_configs = db.relationship('IpmiConfig', backref='author', lazy='dynamic',
                                   cascade='all,delete-orphan', passive_deletes=True)

    def __init__(self, username, email, name, groups, weixin, password, status):

        self.username = username
        self.email = email
        self.name = name
        self.set_groups(groups)
        self.weixin = weixin
        self.password = generate_password_hash(password, salt_length=8)
        self.status = status

    def __repr__(self):
        return '<User %s>' % self.name

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_password(self, new_password):
        self.password = generate_password_hash(new_password, salt_length=8)

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

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Group(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(50))

    def __init__(self, name, desc):

        self.name = name
        self.desc = desc

    def __repr__(self):
        return '<Group %s, %s, %s>' % (self.id, self.name, self.desc)