import unittest
from backfeed_protocol import utils
from webtest import TestApp

from restapi import main


class APITestCase(unittest.TestCase):
    """Base class for testing API functions"""

    contract_name = 'contract1'
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:',
    }

    def setUp(self):
        self.app = TestApp(main({}, **self.settings))
        utils.setup_database(self.settings)
        from backfeed_protocol.models import Base
        from backfeed_protocol.models import DBSession
        engine = DBSession.connection().engine
        Base.metadata.create_all(engine)
        self.contract = utils.get_contract()
        self.url_users_collection = '/{contract}/users'.format(contract=self.contract_name)

    def tearDown(self):
        utils.reset_database()
