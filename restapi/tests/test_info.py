from common import APITestCase


class TestInfo(APITestCase):

    def test_info(self):
        app = self.app
        url = '/_info'
        response = app.get(url)
        self.assertEqual(response.json['engine_url'], 'sqlite:///:memory:')
        self.assertEqual(response.json['settings']['sqlalchemy.url'], 'sqlite:///:memory:')
