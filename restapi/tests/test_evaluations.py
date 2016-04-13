from common import APITestCase


class TestEvaluations(APITestCase):

    def test_workflow(self):
        app = self.app

        url_collection = '/{contract}/evaluations'.format(contract=self.contract_name)

        def url_resource(evaluation_id):
            return '/{contract}/evaluations/{evaluation_id}'.format(
                contract=self.contract_name,
                evaluation_id=evaluation_id,
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
