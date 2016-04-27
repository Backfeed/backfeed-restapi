import sqlalchemy
import logging

from common import APITestCase


class TestWithPostgres(APITestCase):
    """All the other tests run in memory - here we test with files"""

    settings = {
        'sqlalchemy.url': 'postgresql://backfeed-test:backfeed@localhost:5432/backfeed-test',
    }

    def setUp(self):

        try:
            super(TestWithPostgres, self).setUp()
            self.db_ok = True
        except sqlalchemy.exc.OperationalError as error:
            msg = ''
            msg += '\n'
            msg += '*' * 80
            msg += '\n'
            msg += "WARNING: There was an error connecting to the postgres server."
            msg += '\n'
            msg += "For this test to work, you need to set up a test database"
            msg += '\n'
            msg += self.settings['sqlalchemy.url']
            msg += '\n'
            msg += 'See the CONTRIBUTING file for details'
            msg += '\n'
            msg += unicode(error)
            msg += '\n'
            msg += '*' * 80
            self.db_ok = False
            logging.error(msg)

    def test_sanity(self):
        # the connection is made and defined in self.setUp
        if self.db_ok:
            self.assertTrue(self.contract.create_user())
