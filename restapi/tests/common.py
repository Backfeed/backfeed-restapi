import unittest
from restapi import protocol
from webtest import TestApp

from restapi import main


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""
    def setUp(self):
        protocol.setup_database(':memory:')
        self.app = TestApp(main({}))
        self.contract_name = 'contract1'
        self.contract = protocol.get_contract(self.contract_name)
        self.url_users_collection = '/{contract}/users'.format(contract=self.contract_name)

    def tearDown(self):
        protocol.reset_database()
