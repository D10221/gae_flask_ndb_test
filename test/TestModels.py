import unittest

from google.appengine.api import users

from models import Role, LocalUser, set_up_default_roles
from DatastoreTestBase import DatastoreTestCaseBase

import sys
sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(1, '../lib')


def setup_roles():
    Role(id='none', role_id='none', ordinal=0).put()
    Role(id='user', role_id='user', ordinal=1).put()
    Role(id='admin', role_id='admin', ordinal=2).put()


class TestModels(DatastoreTestCaseBase):

    def test_roles(self):
        """ A test """
        role = Role(id='none', role_id='none', ordinal=0)
        self.assertIsNotNone(role)
        role.put()
        found = Role.get_by_id('none')
        self.assertIsNotNone(found)
        self.assertEqual('none', found.key.id())
        self.assertEqual('none', found.role_id)

    def test_user(self):
        user = LocalUser(id='xyz', user_id='xyz', email='no@mail')
        user.put()
        user_found = LocalUser.get_by_id('xyz')
        self.assertIsNotNone(user_found)
        self.assertEqual('xyz', user_found.user_id)

    def test_user_role(self):
        """ A test """
        setup_roles()
        user = LocalUser.new_user(user_id='xyz', email='no@mail', roles=['user'])
        user.put()
        user_found = LocalUser.get_by_id('xyz')
        self.assertIsNotNone(user_found)
        self.assertEqual('xyz', user_found.user_id)
        self.assertEqual('no@mail', user_found.email)
        self.assertEqual('user', Role.get_by_id(user_found.get_role('user').id()).role_id)

        self.assertIsNone(user_found.get_role('admin'))
        self.assertEqual('user', user_found.get_role('user').id())
        self.assertEqual('user', user_found.get_role_id('user'))
        self.assertTrue(user_found.has_role('user'))
        self.assertFalse(user_found.has_role('admin'))

    def test_append_role(self):
        setup_roles()
        user = LocalUser(id='xyz', user_id='xyz', email='no@mail')
        self.assertEqual(0, user.roles.__len__())
        user.add_role('user')
        self.assertEqual('user', user.roles[0].id())

    def test_local_user_from_gae_userl(self):
        self.set_current_user(user_id='1234', email='no@mail')
        user = users.get_current_user()
        self.assertIsNotNone(user)
        local_user = LocalUser.from_gae_user(user)
        self.assertIsNotNone(local_user)
        self.assertEqual('1234', local_user.user_id)

    def test_local_user_from_gae_userl_with_role(self):
        set_up_default_roles()
        self.set_current_user(user_id='1234', email='no@mail')
        user = users.get_current_user()
        self.assertIsNotNone(user)
        local_user = LocalUser.from_gae_user(user, roles=['admin'])
        self.assertIsNotNone(local_user)
        self.assertEqual('1234', local_user.user_id)
        self.assertEqual('admin', local_user.roles[0].id())


class TestMe(unittest.TestCase):
    """ A test """
    def test_me(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
