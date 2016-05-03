import unittest
from backfeed_protocol import utils
from webtest import TestApp

from restapi import main


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""

    contract_name = u'example'
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:',
    }

    def setUp(self):
        self.app = TestApp(main({}, **self.settings))
        utils.setup_database(self.settings)
        self.contract = utils.get_contract(name='example')

    def tearDown(self):
        utils.reset_database()

    @property
    def url_users_collection(self):
        return '/{contract}/users'.format(contract=self.contract_name)
