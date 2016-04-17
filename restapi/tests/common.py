import unittest
from restapi import protocol
from webtest import TestApp

from restapi import main


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""
    def setUp(self):
        sqlite_db = ':memory:'
        protocol.setup_database(sqlite_db)
        self.app = TestApp(main({}, sqlite_db=sqlite_db))
        self.contract_name = 'contract1'
        self.contract = protocol.get_contract(self.contract_name)
        self.url_users_collection = '/{contract}/users'.format(contract=self.contract_name)

    def tearDown(self):
        protocol.reset_database()
