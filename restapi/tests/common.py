import unittest
from webtest import TestApp

from protocol import utils

from restapi import main


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""
    def setUp(self):
        utils.setup_database()
        self.app = TestApp(main({}))
        self.contract_name = 'contract1'
