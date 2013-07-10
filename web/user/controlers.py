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


import re
from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask.ext.login import login_user, logout_user, login_required, current_user

from web import db

from web.user.forms import UserLoginForm, EditUserForm

from web.user.models import User


user = Blueprint('user', __name__)


@user.route('/')
@login_required
def index_ctrl():

    return redirect(url_for('operation.list_operation_ctrl', kind='Ssh'))


@user.route('/login', methods=['GET', 'POST'])
def user_login_ctrl():

    form = UserLoginForm()
    default_next_page = request.values.get('next', url_for('user.index_ctrl'))

    if request.method == 'GET':

        return render_template('user/login.html', form=form)

    elif request.method == 'POST':

        if form.email.data == u'' or form.password.data == u'':

            flash(u'Email and password can\'t be empty', 'error')
            return redirect(url_for('user.user_login_ctrl'))

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and not user.is_active():
            flash(u'User has been disabled', 'error')
            return redirect(url_for('user.user_login_ctrl'))

        elif user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(u'Login successful', 'success')
            return redirect(default_next_page)
        else:
            flash(u'Incorrect email or password', 'error')
            return redirect(url_for('user.user_login_ctrl'))


@user.route('/logout', methods=['GET'])
def user_logout_ctrl():

    logout_user()

    return redirect(url_for('user.index_ctrl'))


@user.route('/settings', methods=("GET", "POST"))
@login_required
def edit_settings_ctrl():

    user = current_user

    form = EditUserForm(email=user.email, name=user.name)

    if request.method == 'GET':

        return render_template('user/settings.html', form=form, type='edit')

    elif request.method == 'POST':

#        if form.email.data != user.email and form.email.data != u'':
#            if User.query.filter_by(email=form.email.data).all():
#                flash(u'The current email is already in use', 'error')
#                return redirect(url_for('user.edit_profile_ctrl'))
#            elif not re.match("^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", form.email.data):
#                flash(u'Incorrect e-mail address', 'error')
#                return redirect(url_for('user.edit_profile_ctrl'))
#            else:
#                user.email = form.email.data

        if form.name.data != user.name and form.name.data != u'':
            if User.query.filter_by(name=form.name.data).all():
                flash(u'The current name is already in use', 'error')
                return redirect(url_for('user.edit_settings_ctrl'))
            elif not re.match("^[a-zA-Z0-9\-\.]{3,20}$", form.email.data):
                flash(u'Incorrect name format', 'error')
                return redirect(url_for('user.edit_settings_ctrl'))
            else:
                user.name = form.name.data

        if len(form.new_password.data) > 0:

            if user.check_password(form.now_password.data):

                if form.new_password.data != form.confirm_password.data:
                    flash(u'Please enter the same password', 'error')
                    return redirect(url_for('user.edit_settings_ctrl'))
                elif not re.match(".{8,20}$", form.new_password.data):
                    flash(u'Incorrect password format', 'error')
                    return redirect(url_for('user.edit_settings_ctrl'))
                else:
                    user.update_password(form.new_password.data)

            else:
                flash(u'Current password is incorrect', 'error')
                return redirect(url_for('user.edit_settings_ctrl'))

        db.session.commit()
        flash(u'Update user settings successfully', 'success')

        return redirect(url_for('user.edit_settings_ctrl'))