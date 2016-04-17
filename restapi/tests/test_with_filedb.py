from common import APITestCase


class TestWithDBFile(APITestCase):
    """All the other tests run in memory - here we test with files"""
    sqlite_db = '/tmp/backfeed_test.db'

    def test_sanity(self):
        # the connection is made and defined in self.setUp
        self.assertTrue(self.contract.create_user())
