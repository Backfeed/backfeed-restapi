from common import APITestCase


class TestUsers(APITestCase):

    def url_resource(self, user_id):
        return '/{contract}/users/{user_id}'.format(
            contract=self.contract_name,
            user_id=user_id,
        )

    @property
    def url_collection(self):
        return '/{contract}/users'.format(contract=self.contract_name)

    def test_workflow(self):
        app = self.app
        url_collection = self.url_collection
        url_resource = self.url_resource

        # create a user
        response = app.post(url_collection, {'tokens': 10})
        self.assertEqual(response.json['tokens'], 10)

        # update a user
        user_id = response.json['id']
        response = app.put(url_resource(user_id), {'tokens': 20})
        self.assertEqual(response.json['tokens'], 20)

        # get the user info
        response = app.get(url_resource(user_id))

        # get the user collection
        response = app.get(url_collection)
        self.assertEqual(response.json.get('count'), 1)

        # delete user
        response = app.delete(url_resource(user_id))
        response = app.get(url_collection)
        self.assertEqual(response.json.get('count'), 0)

    def test_reputation(self):
        user1 = self.contract.create_user(reputation=10)
        self.contract.create_user(reputation=30)

        user_info = self.app.get(self.url_resource(user1.id)).json
        self.assertEqual(user_info['reputation'], 0.25)
