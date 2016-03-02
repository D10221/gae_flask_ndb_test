from google.appengine.api import users

# from authentication import requires_login
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
# @requires_login
def hello_world():
    current_user = users.get_current_user()
    return render_template('index.html', user=current_user)
