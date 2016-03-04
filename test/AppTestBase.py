#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

TODO: These tests need to be updated to support the Python 2.7 runtime

source : https://raw.githubusercontent.com/kamalgill/flask-appengine-template/master/src/tests/tests.py
"""
import os
import unittest

from google.appengine.api import users

import config

from google.appengine.ext import testbed

from main import app


class AppTestBase(unittest.TestCase):
    def setUp(self):
        # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
        app.config.from_pyfile(os.path.join(config.BASE_DIR, 'config.py'))
        self.flask_app = app
        self.app = app.test_client()
        # Setups app engine test bed.
        # See: http://code.google.com/
        # appengine/docs/python/tools/localunittesting.html#Introducing_the_Python_Testing_Utilities
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def set_current_user(self, email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

    def set_and_get_current_user(self, email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'
        return users.get_current_user()

