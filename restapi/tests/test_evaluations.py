from common import APITestCase
from ..views.config import URL_EVALUATION_COLLECTION, URL_EVALUATION_RESOURCE


class TestEvaluations(APITestCase):
    @property
    def url_collection(self):
        return URL_EVALUATION_COLLECTION.format(contract=self.contract_name)

    def url_resource(self, evaluation_id):
            return URL_EVALUATION_RESOURCE.format(
                contract=self.contract_name,
                id=evaluation_id,
            )

    def test_workflow(self):
        # test creating and getting evaluations
        app = self.app

        # create a user and a contribution to evaluate
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)

        # create an evaluation
        response = app.post(
            self.url_collection,
            {
                'evaluator_id': user.id,
                'contribution_id': contribution.id,
                'value': 1,
            }
        )
        self.assertEqual(response.json['value'], 1)
        evaluation_id = response.json['id']

        # get the evaluation info
        response = app.get(self.url_resource(evaluation_id))

        # get the evaluation collection
        response = app.get(self.url_collection)
        self.assertEqual(response.json.get('count'), 1)

    def test_evaluation_get(self):
        # test that GETting an evaluation returns all expected data
        user = self.contract.create_user(tokens=100, reputation=3.141)
        # create another user just to make the numbers more meaningful
        self.contract.create_user(reputation=3.141)
        contribution = self.contract.create_contribution(user=user)
        evaluation = self.contract.create_evaluation(
            contribution=contribution, value=1, user=user)

        url = URL_EVALUATION_RESOURCE.format(id=evaluation.id, contract=self.contract_name)
        info = self.app.get(url).json
        self.assertEqual(info['value'], 1)
        self.assertEqual(info['contribution']['id'], contribution.id)
        self.assertEqual(info['contribution']['stats']['engaged_reputation'], user.relative_reputation())
        self.assertGreater(info['contribution']['stats']['score'], 0)
        self.assertEqual(info['evaluator']['id'], user.id)
        self.assertEqual(info['evaluator']['tokens'], 99)
        self.assertEqual(info['evaluator']['reputation_normalized'], user.relative_reputation())
        self.assertEqual(info['evaluator']['reputation'], user.reputation)

    def test_evaluation_post(self):
        # test that GETting an evaluation returns all expected data
        user = self.contract.create_user(tokens=100, reputation=3.141)
        # create another user just to make the numbers more meaningful
        self.contract.create_user(reputation=3.141)
        contribution = self.contract.create_contribution(user=user)
        data = dict(contribution_id=contribution.id, value=1, evaluator_id=user.id)

        url = self.url_collection
        info = self.app.post(url, data).json
        self.assertEqual(info['value'], 1)
        self.assertEqual(info['contribution']['id'], contribution.id)
        self.assertEqual(info['contribution']['stats']['engaged_reputation'], user.relative_reputation())
        self.assertGreater(info['contribution']['stats']['score'], 0)
        self.assertEqual(info['evaluator']['id'], user.id)
        self.assertEqual(info['evaluator']['tokens'], 99)
        self.assertEqual(info['evaluator']['reputation_normalized'], user.relative_reputation())
        self.assertEqual(info['evaluator']['reputation'], user.reputation)

    def test_evaluation_collection_get(self):
        # add some data
        user0 = self.contract.create_user()
        user1 = self.contract.create_user()
        contribution0 = self.contract.create_contribution(user=user0)
        contribution1 = self.contract.create_contribution(user=user1)
        self.contract.create_evaluation(contribution=contribution0, value=1, user=user0)
        self.contract.create_evaluation(contribution=contribution0, value=1, user=user1)
        self.contract.create_evaluation(contribution=contribution1, value=1, user=user0)

        response = self.app.get(self.url_collection)
        self.assertEqual(response.json.get('count'), 3)
        response = self.app.get(self.url_collection, {'contribution_id': contribution0.id})
        self.assertEqual(response.json.get('count'), 2)
        response = self.app.get(self.url_collection, {'evaluator_id': user0.id})
        self.assertEqual(response.json.get('count'), 2)
        response = self.app.get(self.url_collection, {'evaluator_id': user1.id})
        self.assertEqual(response.json.get('count'), 1)
        response = self.app.get(self.url_collection, {'evaluator_id': 12345})
        self.assertEqual(response.json.get('count'), 0)

        # test error handling
        response = self.app.get(self.url_collection, {'evaluator_id': 'xx'}, expect_errors=True)
        self.assertEqual(response.status, '400 Bad Request')

    def test_evaluation_errors(self):
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)

        # try to create an evaluation with an illegal value
        response = self.app.post(
            self.url_collection,
            {
                'evaluator_id': user.id,
                'contribution_id': contribution.id,
                'value': 10000,
            },
            expect_errors=True,
        )
        self.assertEqual(response.status, '400 Bad Request')

    def test_errors_resource(self):
        response = self.app.get(self.url_resource(123455), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get(self.url_resource('astring'), expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def test_errors_collection(self):
        response = self.app.get(self.url_collection, {'nonexisting': '1'}, expect_errors=True)
        self.assertEqual(response.status_code, 400)
