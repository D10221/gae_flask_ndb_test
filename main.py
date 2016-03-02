from google.appengine.api import users

from authentication import requires_login, requires_role
from flask import Flask, render_template, redirect


app = Flask(__name__)


@app.route('/')
@requires_login
def hello_world():
    current_user = users.get_current_user()
    return render_template('index.html', user=current_user)


@app.route('/logout')
def logout():
    return redirect(users.create_logout_url('/login'))


@app.route('/login')
def login():
    return redirect(users.create_login_url('/'))


@app.route('/admin')
@requires_role('admin', '/authorize')
def admin():
    return 'admin'


@app.route('/authorize')
@requires_login
def authorize():
    return "TODO:"
