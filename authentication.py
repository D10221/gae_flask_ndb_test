from flask import redirect
from functools import wraps

from google.appengine.api import users


def requires_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = users.get_current_user()
        if user is None:
            return redirect(users.create_login_url('/'))
        return func(*args, **kwargs)
    # ...
    return wrapper
