import types
from datetime import datetime
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
        self.assertEqual(response.json['_meta']['total'], 1)

    def test_data(self):
        user = self.contract.create_user(reputation=3.141)
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
        self.assertEqual(data['contributor']['reputation_normalized'], 1.0)
        self.assertEqual(data['type'], 'article')
        self.assertItemsEqual(data['stats']['evaluations'].keys(), ['1', '0'])
        self.assertEqual(data['stats']['quality'], self.contract.contribution_quality(contribution))

        # they should be the same as those returned by the GET request
        data_get = self.app.get(self.url_resource(contribution_id)).json
        self.assertEqual(data, data_get)

        # now check if we get the right statistics
        evaluator = self.contract.create_user(reputation=3.141)
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

    def test_create(self):
        # test for parameters and error handling
        user = self.contract.create_user()
        response = self.app.post(self.url_collection, {'contributor_id': user.id})
        self.assertEqual(response.status_code, 200)
        response = self.app.post(
            self.url_collection,
            {'contributor_id': user.id, 'type': 'comment'},
            expect_errors=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['type'], 'comment')
        response = self.app.post(
            self.url_collection,
            {'contributor_id': user.id, 'type': 'somethingthatdoesnotexist'},
            expect_errors=True
        )
        self.assertEqual(response.status_code, 400)

    def test_collection_get(self):
        # have some data to test with
        contract = self.contract
        user0 = contract.create_user(reputation=3.141)
        user1 = contract.create_user(reputation=3.141)

        contribution0 = contract.create_contribution(user=user0)
        contribution1 = contract.create_contribution(user=user0)
        contribution2 = contract.create_contribution(user=user1)
        contribution0.time = datetime(2010, 1, 1)
        contribution1.time = datetime(2011, 1, 1)
        contribution2.time = datetime(2012, 1, 1)

        # add some evaluations to determine the score
        contract.create_evaluation(contribution=contribution1, user=user0, value=1)
        contract.create_evaluation(contribution=contribution2, user=user0, value=1)
        contract.create_evaluation(contribution=contribution2, user=user1, value=1)

        app = self.app
        url = self.url_collection

        #
        # test _meta info
        #
        result = app.get(url).json
        self.assertEqual(result['_meta']['total'], 3)
        self.assertEqual(result['_meta']['start'], 0)
        self.assertEqual(len(result['items']), 3)

        result = app.get(url, {'limit': 1}).json
        self.assertEqual(len(result['items']), 1)

        result = app.get(url, {'start': 2}).json
        self.assertEqual(result['_meta']['start'], 2)
        self.assertEqual(len(result['items']), 1)

        # check ordering - we have set up things such that
        # the contribution2 has the highest score, and contribution0 the lowest
        result = app.get(url).json
        self.assertEqual(result['items'][0]['id'], contribution2.id)
        self.assertEqual(result['items'][2]['id'], contribution0.id)

        result = app.get(url, {'order_by': '-score'}).json
        self.assertEqual(result['items'][0]['id'], contribution2.id)
        self.assertEqual(result['items'][2]['id'], contribution0.id)

        result = app.get(url, {'order_by': 'time'}).json
        self.assertEqual(result['items'][0]['id'], contribution0.id)
        self.assertEqual(result['items'][2]['id'], contribution2.id)

        result = app.get(url, {'order_by': '-time'}).json
        self.assertEqual(result['items'][0]['id'], contribution2.id)
        self.assertEqual(result['items'][2]['id'], contribution0.id)

        #
        # test querying
        #
        contract.create_contribution(user=user1, contribution_type='comment')
        response = self.app.get(url, {'type': 'comment'})
        self.assertEqual(len(response.json['items']), 1)
        self.assertEqual(response.json['_meta']['total'], 1)

        response = self.app.get(url, {'type': 'article'})
        self.assertEqual(len(response.json['items']), 3)
        self.assertEqual(response.json['_meta']['total'], 3)

    def test_errors(self):
        response = self.app.get(self.url_resource(123455), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get(self.url_resource('astring'), expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def test_errors_collection(self):
        response = self.app.get(self.url_collection, {'nonexisting': '1'}, expect_errors=True)
        self.assertEqual(response.status_code, 400)
