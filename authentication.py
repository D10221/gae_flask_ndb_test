from flask import redirect, request, abort
from functools import wraps
import config

from google.appengine.api import users

from models import LocalUser


def requires_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = users.get_current_user()
        if user is None:
            return redirect(users.create_login_url('/'), request.url) \
                if config.ON_MISSING_ROLE['login'] is None else \
                abort(config.ON_MISSING_ROLE['login'])
        return func(*args, **kwargs)

    # ...
    return wrapper


def requires_role(role, redirected=None):
    def wrapper(f):
        @wraps(f)
        def sub(*args, **kwargs):
            user = users.get_current_user()
            local_user = None if user is None else LocalUser.get_by_id(user.user_id())
            if local_user and local_user.has_role(role):
                return f(*args, **kwargs)
            if redirected is None:
                abort(401)
            return redirect(redirected)

        return sub

    return wrapper
