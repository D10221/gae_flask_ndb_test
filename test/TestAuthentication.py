from google.appengine.api import users
from werkzeug.exceptions import Unauthorized

from authentication import requires_role, requires_login
from models import LocalUser, set_up_default_roles
from test.AppTestBase import AppTestBase


class TestAuthentication(AppTestBase):

    def test_requires_role_throws(self):
        error = None

        @requires_role('admin')
        def ok(to_return):
            return to_return
        try:
            ok('x')
        except Unauthorized as e:
            error = e
        # call should no t succeed
        self.assertIsNotNone(error)

    def test_requires_role_ok(self):
        error = None
        set_up_default_roles()
        self.set_current_user(user_id='user', email='user@email')
        user = users.get_current_user()
        local_user = LocalUser.from_gae_user(user, roles=['admin'])
        local_user.put()

        result = None

        @requires_role('admin')
        def ok(to_return):
            return to_return
        try:
            result = ok('x')
        except Unauthorized as e:
            error = e
        # call should succeed
        self.assertIsNone(error)
        self.assertEqual('x', result)

    def test_requires_login(self):
        self.set_current_user(user_id='user', email='user@email')

        @requires_login
        def login():
            return True

        self.assertTrue(login())

    def test_requires_login_denies_access(self):

        @self.flask_app.route('/logintest')
        @requires_login
        def logintest():
            return True
        res = self.app.get('/logintest')
        self.assertEqual(res.status, '401 UNAUTHORIZED')


