import os

from common import APITestCase


class TestWithDBFile(APITestCase):
    """All the other tests run in memory - here we test with files"""

    sqlite_db = '/tmp/backfeedtest.db'
    settings = {
        'sqlalchemy.url': 'sqlite:///{sqlite_db}'.format(sqlite_db=sqlite_db),
    }

    def setUp(self):
        if os.path.exists(self.sqlite_db):
            os.remove(self.sqlite_db)
        super(TestWithDBFile, self).setUp()

    def tearDown(self):
        if os.path.exists(self.sqlite_db):
            os.remove(self.sqlite_db)

    def test_sanity(self):
        # the connection is made and defined in self.setUp
        self.assertTrue(self.contract.create_user())
        self.assertTrue(os.path.exists(self.sqlite_db))
