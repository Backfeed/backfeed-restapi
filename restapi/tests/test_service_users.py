from webtest import TestApp
from restapi import main
from common import APITestCase


class TestUsers(APITestCase):

    def setUp(self):
        super(TestUsers, self).setUp()
        self.contract1_name = 'contract1'

    def test_case(self):
        app = TestApp(main({}))
        response = app.get('/{contract1_name}/users'.format(contract1_name=self.contract1_name))
        self.assertEqual(response.json.get('count'), 0)
        self.assertEqual(response.json.get('items'), [])
