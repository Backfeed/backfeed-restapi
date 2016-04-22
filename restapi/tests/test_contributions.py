from common import APITestCase
from ..views.config import URL_CONTRIBUTION_RESOURCE, URL_CONTRIBUTION_COLLECTION


class TestContributions(APITestCase):

    def url_resource(self, contribution_id):
        return URL_CONTRIBUTION_RESOURCE.format(
            contract=self.contract_name,
            id=contribution_id,
        )

    @property
    def url_collection(self):
        return URL_CONTRIBUTION_COLLECTION.format(contract=self.contract_name)

    def test_workflow(self):
        app = self.app

        # create a user
        user = self.contract.create_user()

        # create a contribution
        response = app.post(self.url_collection, {'contributor_id': user.id})
        self.assertEqual(response.json['contributor']['id'], user.id)
        contribution_id = response.json['id']

        # update a contribution
        # response = app.put(url_resource(contribution_id), {'tokens': 20})
        # self.assertEqual(response.json['tokens'], 20)

        # get the contribution info
        response = app.get(self.url_resource(contribution_id))
        self.assertEqual(response.json['contributor']['id'], user.id)

        # get the contribution collection
        response = app.get(self.url_collection)
        self.assertEqual(response.json.get('count'), 1)

        # delete a contribution (this actually never happens)
        # response = app.delete(url_resource(contribution_id))
        # response = app.get(url_collection)
        # self.assertEqual(response.json.get('count'), 0)

    def test_data(self):
        user = self.contract.create_user()
        # contribution = self.contract.create_contribution(user=user)

        # check the data returned by POST request
        response = self.app.post(self.url_collection, {'contributor_id': user.id})
        data = response.json

        self.assertTrue(data['id'])
        self.assertEqual(data['score'], 0.0)
        self.assertEqual(data['engaged_reputation'], 0)
        self.assertEqual(data['contributor']['id'], user.id)
        self.assertEqual(data['contributor']['tokens'], 49.0)
        self.assertEqual(data['contributor']['reputation'], 1.0)
        self.assertEqual(data['type'], 'article')

        # they should be the same as those returned by the GET request
        data_get = self.app.get(self.url_resource(data['id'])).json
        self.assertEqual(data, data_get)
