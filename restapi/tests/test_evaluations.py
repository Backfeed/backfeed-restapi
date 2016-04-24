from common import APITestCase
from ..views.config import URL_EVALUATION_COLLECTION, URL_EVALUATION_RESOURCE


class TestEvaluations(APITestCase):
    @property
    def url_collection(self):
        return URL_EVALUATION_COLLECTION.format(contract=self.contract_name)

    def test_workflow(self):
        # test creating and getting evaluations
        app = self.app

        def url_resource(evaluation_id):
            return URL_EVALUATION_RESOURCE.format(
                contract=self.contract_name,
                id=evaluation_id,
            )

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
        response = app.get(url_resource(evaluation_id))

        # get the evaluation collection
        response = app.get(self.url_collection)
        self.assertEqual(response.json.get('count'), 1)

    def test_evaluation_data(self):
        # test that GETting an evaluation returns all expected data
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        evaluation = self.contract.create_evaluation(
            contribution=contribution, value=1, user=user)

        url = URL_EVALUATION_RESOURCE.format(id=evaluation.id, contract=self.contract_name)
        info = self.app.get(url).json
        self.assertEqual(info['value'], 1)
        self.assertEqual(info['contribution']['id'], contribution.id)
        self.assertEqual(info['contribution']['score'], 1.0)
        self.assertEqual(info['contribution']['engaged_reputation'], user.reputation)
        self.assertEqual(info['evaluator']['id'], user.id)
        self.assertEqual(info['evaluator']['tokens'], 99)
        self.assertEqual(info['evaluator']['reputation'], 1)

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
