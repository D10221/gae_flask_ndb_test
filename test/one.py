import unittest

from models import Role, LocalUser
from test_base import DatastoreTestCase


def setup_roles():
    Role(id='none', role_id='none', ordinal=0).put()
    Role(id='user', role_id='user', ordinal=1).put()
    Role(id='admin', role_id='admin', ordinal=2).put()


class TestModels(DatastoreTestCase):

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
        # fail
        self.assertIsNone(user_found.get_role('admin'))
        self.assertEqual('user', user_found.get_role('user').id())
        self.assertEqual('user', user_found.get_role_id('user'))
        self.assertTrue(user_found.has_role('user'))
        self.assertFalse(user_found.has_role('admin'))


class TestMe(unittest.TestCase):
    """ A test """
    def test_me(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
