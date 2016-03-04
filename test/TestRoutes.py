from google.appengine.api import users

from models import LocalUser, set_up_default_roles
from test.AppTestBase import AppTestBase


class TestRoutes(AppTestBase):

    def test_home(self):
        self.set_current_user('me@me', '1234')
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_home_nouser(self):
        rv = self.app.get('/')
        assert rv.status == '401 UNAUTHORIZED'

    # def test_inserts_data(self):
    #     self.set_current_user(u'john@example.com', u'123')
    #     rv = self.app.post('/examples', data=dict(
    #         example_name='An example',
    #         example_description='Description of an example'
    #     ), follow_redirects=True)
    #     assert 'successfully saved' in rv.data
    #
    #     rv = self.app.get('/examples')
    #     assert 'No examples yet' not in rv.data
    #     assert 'An example' in rv.data

    def test_admin_logins_ok(self):
        # Normal user
        set_up_default_roles()
        self.set_current_user(u'john@example.com', u'123')
        LocalUser.from_gae_user(
            users.get_current_user(),
            roles=['admin']).put()
        rv = self.app.get('/admin')
        assert rv.status == '200 OK'

    def test_admin_login_not_ok(self):
        # Anonymous
        rv = self.app.get('/admin')
        # in test we got unauthorized , app can't find route to users.get_login_url()
        assert rv.status == '401 UNAUTHORIZED'

    def test_404(self):
        rv = self.app.get('/missing')
        assert rv.status == '404 NOT FOUND'

    def test_authorize(self):
        set_up_default_roles()
        current_user = self.set_and_get_current_user('admin@root', 'admin')
        LocalUser.from_gae_user(current_user, roles=['admin']).put()
        LocalUser.new_user(user_id='me', email='me@mail').put()
        res = self.app.get('/user/me@mail/role/add/admin')
        self.assertEqual('admin', res.data)

    def test_authorize_fails(self):
        LocalUser.new_user(user_id='me', email='me@mail').put()
        res = self.app.get('/user/me@mail/role/add/admin')
        self.assertEqual('401 UNAUTHORIZED', res.status)
