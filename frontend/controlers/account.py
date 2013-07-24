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
from flask import render_template, request, flash, redirect, url_for, Blueprint, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from frontend.forms.account import UserLoginForm, EditSettingForm

from frontend.models.account import User

from frontend.extensions.database import db
from frontend.extensions.utility import catch_errors


account = Blueprint('account', __name__)


@account.route('/')
@login_required
def index_ctrl():

    return redirect(url_for('operation.list_operation_ctrl', operation_type='ssh_detect'))


@account.route('/login', methods=['GET', 'POST'])
def user_login_ctrl():

    form = UserLoginForm()
    default_next_page = request.values.get('next', url_for('account.index_ctrl'))

    if request.method == 'GET':
        return render_template('account/login.html', form=form)

    elif request.method == 'POST' and form.validate():

        user = User.query.filter(or_(User.email == form.key_name.data, User.username == form.key_name.data)).first()

        if user is None:
            flash(u'User does not exist', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        elif not user.is_active():
            flash(u'User has been disabled', 'error')
            return redirect(url_for('account.user_login_ctrl'))

        elif user.check_password(form.password.data):

            login_user(user)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

            flash(u'Login successful', 'success')
            return redirect(default_next_page)

        else:
            flash(u'Current password is incorrect', 'error')
            return redirect(url_for('account.user_login_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.user_login_ctrl'))


@account.route('/logout')
def user_logout_ctrl():

    logout_user()

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('account.index_ctrl'))


@account.route('/settings', methods=("GET", "POST"))
@login_required
def user_edit_settings_ctrl():

    user = current_user
    form = EditSettingForm(id=user.id, email=user.email, username=user.username, name=user.name)

    if request.method == 'GET':
        return render_template('account/change_settings.html', form=form, type='edit')

    elif request.method == 'POST' and form.validate():

        if form.name.data != user.name:
            user.name = form.name.data

        if not user.check_password(form.now_password.data):
            flash(u'Current password is incorrect', 'error')
            return redirect(url_for('account.user_edit_settings_ctrl'))
        else:
            user.update_password(form.new_password.data)

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

        return redirect(url_for('account.user_edit_settings_ctrl'))

    else:
        messages = catch_errors(form.errors)

        flash(messages, 'error')
        return redirect(url_for('account.user_edit_settings_ctrl'))