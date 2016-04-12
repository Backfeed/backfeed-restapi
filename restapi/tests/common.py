import unittest

from protocol import utils


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""
    def setUp(self):
        utils.setup_database()
