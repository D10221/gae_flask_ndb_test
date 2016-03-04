import unittest

from TestAuthentication import TestAuthentication
from TestModels import TestModels
from TestRoutes import TestRoutes


__all__ = [TestAuthentication, TestModels, TestRoutes]

for a in __all__:
    suite = unittest.TestLoader().loadTestsFromTestCase(a)

unittest.TextTestRunner(verbosity=2).run(suite)