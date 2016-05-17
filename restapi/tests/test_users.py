from ..views import config
from common import APITestCase


class TestUsers(APITestCase):

    def url_resource(self, user_id):
        return config.URL_USER_RESOURCE.format(
            contract=self.contract_name,
            id=user_id,
        )

    @property
    def url_collection(self):
        return config.URL_USER_COLLECTION.format(contract=self.contract_name)

    def test_workflow(self):
        app = self.app
        url_collection = self.url_collection
        url_resource = self.url_resource

        # create a user
        response = app.post(url_collection, {'tokens': 10})
        self.assertEqual(response.json['tokens'], 10)
        user_id = response.json['id']

        # update a user
        # response = app.put(url_resource(user_id), {'tokens': 20})
        # self.assertEqual(response.json['tokens'], 20)

        # get the user info
        response = app.get(url_resource(user_id))

        # get the user collection
        response = app.get(url_collection)
        self.assertEqual(response.json['_meta']['total'], 1)

    def test_user_info(self):
        user1 = self.contract.create_user(reputation=10)
        self.contract.create_user(reputation=30)

        response = self.app.get(self.url_resource(user1.id))
        # reputation should be returned as a fraction of the total reputation
        self.assertEqual(response.json['reputation_normalized'], 0.25)
        self.assertEqual(response.json['reputation'], 10)
        self.assertEqual(response.json['total_reputation'], 40)

    def test_user_collection_get(self):
        self.contract.create_user()
        response = self.app.get(self.url_collection)
        self.assertEqual(response.json['_meta']['start'], 0)
        self.assertEqual(response.json['_meta']['total'], 1)

    def test_user_creation(self):
        app = self.app
        url_collection = self.url_collection
        # create a user
        response = app.post(url_collection, {'tokens': 10, 'reputation': 3.141})
        self.assertEqual(response.json['tokens'], 10)
        # returns the *relative* reputation
        self.assertEqual(response.json['reputation_normalized'], 1.0)
        self.assertEqual(response.json['reputation'], 3.141)
        self.assertEqual(response.json['total_reputation'], 3.141)
        user_id = response.json['id']

        # create a referring user
        response = app.post(url_collection, {'referrer_id': user_id})
        self.assertEqual(response.json['referrer']['id'], user_id)

        # try with a non-exising reference
        response = app.post(url_collection, {'referrer_id': 123456}, expect_errors=True)
        self.assertEqual(response.status, '400 Bad Request')

    def test_errors(self):
        response = self.app.get(self.url_resource(123455), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get(self.url_resource('astring'), expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def test_errors_collection(self):
        response = self.app.get(self.url_collection, {'nonexisting': '1'}, expect_errors=True)
        self.assertEqual(response.status_code, 400)
