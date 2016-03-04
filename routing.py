from flask import render_template, redirect, render_template_string, request
from google.appengine.api import users

import config
from authentication import requires_login, requires_role
from models import LocalUser


def init_app(app):
    @app.route('/')
    @requires_login
    def root():
        current_user = users.get_current_user()
        return render_template('index.html', user=current_user)

    @app.route('/logout')
    def logout():
        return redirect(users.create_logout_url('/login'))

    @app.route('/login')
    def login():
        return redirect(users.create_login_url('/'))

    @app.route('/admin')
    @requires_role('admin', config.ON_MISSING_ROLE['admin'])
    def admin():
        return 'admin'

    @app.route('/user/<user_email>/role/add/<role>')
    @requires_role('admin')
    def authorize(user_email, role):
        user = LocalUser.query(LocalUser.email == user_email).get()
        user.add_role(role)
        return user.get_role_id(role)

    @app.route('/whomi')
    def whomi():
        return render_template_string(
            'you are: {{user}}',
            user=users.get_current_user().email())
