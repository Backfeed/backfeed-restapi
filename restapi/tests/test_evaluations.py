from common import APITestCase
from ..views.config import URL_EVALUATION_COLLECTION, URL_EVALUATION_RESOURCE


class TestEvaluations(APITestCase):

    def test_workflow(self):
        # test creating and getting evaluations
        app = self.app

        url_collection = URL_EVALUATION_COLLECTION.format(contract=self.contract_name)

        def url_resource(evaluation_id):
            return URL_EVALUATION_RESOURCE.format(
                contract=self.contract_name,
                id=evaluation_id,
            )

        # create a user and a contribution to evaluate
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)

        # create a evaluation
        response = app.post(
            url_collection,
            {
                'user_id': user.id,
                'contribution_id': contribution.id,
                'value': 10,
            }
        )
        self.assertEqual(response.json['value'], 10)
        evaluation_id = response.json['id']

        # get the evaluation info
        response = app.get(url_resource(evaluation_id))

        # get the evaluation collection
        response = app.get(url_collection)
        self.assertEqual(response.json.get('count'), 1)

    def test_evaluation_data(self):
        # test that GETting an evaluation returns all expected data
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        value = 3.14
        evaluation = self.contract.create_evaluation(
            contribution=contribution, value=value, user=user)

        url = URL_EVALUATION_RESOURCE.format(id=evaluation.id, contract=self.contract_name)
        info = self.app.get(url).json
        self.assertEqual(info['value'], value)
        self.assertEqual(info['contribution']['id'], contribution.id)
        self.assertEqual(info['contribution']['score'], 0.0)
        self.assertEqual(info['contribution']['engaged_reputation'], user.reputation)
        self.assertEqual(info['evaluator']['id'], user.id)
        self.assertEqual(info['evaluator']['tokens'], 49)
        self.assertEqual(info['evaluator']['reputation'], 1)
