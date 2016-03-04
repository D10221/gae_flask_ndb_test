# Copyright 2015 Google Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

#    source = https://raw.githubusercontent.com/
#               GoogleCloudPlatform/python-docs-samples/
#               master/appengine/localtesting/test_datastore.py

# [START imports]
import os
import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


# [END imports]


# [START datastore_example_1]

def get_entity_via_memcache(entity_key):
    """Get entity from memcache if available, from datastore if not.
    :param entity_key:
    """
    entity = memcache.get(entity_key)
    if entity is not None:
        return entity
    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


# [END datastore_example_1]


# [START datastore_example_test]
class DatastoreTestCaseBase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    # [END datastore_example_test]

    # [START datastore_example_teardown]
    def tearDown(self):
        self.testbed.deactivate()

    # [END datastore_example_teardown]

    # Helpers
    def set_current_user(self, email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

# [START HRD_example_1]
from google.appengine.datastore import datastore_stub_util  # noqa


class HighReplicationTestCaseOne(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Create a consistency policy that will simulate the High Replication
        # consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        # Initialize memcache stub too, since ndb also uses memcache
        self.testbed.init_memcache_stub()
        # Clear in-context cache before each test.
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    # [END HRD_example_1]
