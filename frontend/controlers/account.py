#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/01/17.
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


from sqlalchemy import or_
from flask import render_template, request, flash, redirect, url_for, Blueprint, current_app, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from frontend.forms.account import UserLoginForm, EditUserForm

from frontend.models.account import User

from frontend.extensions.database import db
from frontend.extensions.utility import validate_name, validate_password


account = Blueprint('account', __name__)


@account.route('/')
@login_required
def index_ctrl():

    return redirect(url_for('operation.list_operation_ctrl', kind='ssh_detect'))


@account.route('/login', methods=['GET', 'POST'])
def user_login_ctrl():

    form = UserLoginForm()
    default_next_page = request.values.get('next', url_for('account.index_ctrl'))

    if request.method == 'GET':

        return render_template('account/login.html', form=form)

    elif request.method == 'POST':

        if form.key_name.data == u'' or form.password.data == u'':

            flash(u'Email and password can\'t be empty', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        user = User.query.filter(or_(User.email == form.key_name.data, User.username == form.key_name.data)).first()

        if user is None:
            flash(u'Incorrect email or password', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        elif not user.is_active():
            flash(u'User has been disabled', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        elif user.check_password(form.password.data):

            login_user(user)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

            flash(u'Login successful', 'success')
            return redirect(default_next_page)


@account.route('/logout', methods=['GET'])
def user_logout_ctrl():

    logout_user()

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('account.index_ctrl'))


@account.route('/settings', methods=("GET", "POST"))
@login_required
def user_edit_settings_ctrl():

    user = current_user

    form = EditUserForm(email=user.email, username=user.username)

    if request.method == 'GET':

        return render_template('account/change_settings.html', form=form, type='edit')

    elif request.method == 'POST':

        if form.email.data != user.email:
            flash(u'The email can\'t be modified', 'error')
            return redirect(url_for('account.user_edit_settings_ctrl'))

        if form.username.data != user.username and form.username.data != u'':
            if User.query.filter_by(username=form.username.data).all():
                flash(u'The current username is already in use', 'error')
                return redirect(url_for('account.user_edit_settings_ctrl'))
            elif not validate_name(form.username.data):
                flash(u'Incorrect username format', 'error')
                return redirect(url_for('account.user_edit_settings_ctrl'))
            else:
                user.username = form.username.data

        if form.name.data != user.name and form.name.data != u'':
            if User.query.filter_by(name=form.name.data).all():
                flash(u'The current name is already in use', 'error')
                return redirect(url_for('account.user_edit_settings_ctrl'))
            else:
                user.name = form.name.data

        if len(form.new_password.data) > 0:

            if user.check_password(form.now_password.data):
                flash(u'Please enter current password', 'error')
                return redirect(url_for('account.user_edit_settings_ctrl'))
            elif form.new_password.data != form.confirm_password.data:
                flash(u'Please enter the same password', 'error')
                return redirect(url_for('account.user_edit_settings_ctrl'))
            elif not validate_password(form.new_password.data):
                flash(u'Incorrect password format', 'error')
                return redirect(url_for('account.user_edit_settings_ctrl'))
            else:
                user.update_password(form.new_password.data)

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

        return redirect(url_for('account.user_edit_settings_ctrl'))