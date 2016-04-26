import types

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
        contribution_id = data['id']
        contribution = self.contract.get_contribution(contribution_id)

        self.assertTrue(data['id'])
        self.assertEqual(data['stats']['score'], 0.0)
        self.assertEqual(data['stats']['engaged_reputation'], 0)
        self.assertEqual(data['contributor']['id'], user.id)
        self.assertEqual(data['contributor']['tokens'], 49.0)
        self.assertEqual(data['contributor']['reputation'], 1.0)
        self.assertEqual(data['type'], 'article')
        self.assertEqual(data['stats']['evaluations'], {})

        # they should be the same as those returned by the GET request
        data_get = self.app.get(self.url_resource(contribution_id)).json
        self.assertEqual(data, data_get)

        # now check if we get the right statistics
        evaluator = self.contract.create_user()
        self.contract.create_evaluation(contribution=contribution, user=evaluator, value=1)
        evaluator = self.contract.create_user()
        self.contract.create_evaluation(contribution=contribution, user=evaluator, value=0)

        data = self.app.get(self.url_resource(contribution_id)).json
        self.assertEqual(type(data['stats']['evaluations']['0']['reputation']), types.FloatType)
        self.assertEqual(type(data['stats']['evaluations']['1']['reputation']), types.FloatType)

        # check also if we have normalized the reputation
        # (i.e. it should be between 0 and 1)
        self.assertLess(data['stats']['engaged_reputation'], 1.0)
        self.assertLess(data['stats']['evaluations']['0']['reputation'], 1.0)
        self.assertLess(data['stats']['evaluations']['1']['reputation'], 1.0)
