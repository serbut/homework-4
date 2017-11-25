# -*- coding: utf-8 -*-

import sys
import unittest
from tests.photos_test import photos_tests

if __name__ == '__main__':
    suite = unittest.TestSuite((
        photos_tests
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
