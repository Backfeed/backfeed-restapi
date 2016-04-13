import unittest
from webtest import TestApp

from protocol import utils
import protocol
from restapi import main


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""
    def setUp(self):
        utils.setup_database()
        self.app = TestApp(main({}))
        self.contract_name = 'contract1'
        self.contract = protocol.get_contract(self.contract_name)
        self.url_users_collection = '/{contract}/users'.format(contract=self.contract_name)
