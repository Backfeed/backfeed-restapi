from common import APITestCase


class TestContributions(APITestCase):

    def test_workflow(self):
        app = self.app

        url_collection = '/{contract}/contributions'.format(contract=self.contract_name)

        def url_resource(contribution_id):
            return '/{contract}/contributions/{contribution_id}'.format(
                contract=self.contract_name,
                contribution_id=contribution_id,
            )

        # create a user
        response = app.post(self.url_users_collection)
        user_id = response.json['id']

        # create a contribution
        response = app.post(url_collection, {'user_id': user_id})
        self.assertEqual(response.json['user_id'], user_id)
        contribution_id = response.json['id']

        # update a contribution
        # response = app.put(url_resource(contribution_id), {'tokens': 20})
        # self.assertEqual(response.json['tokens'], 20)

        # get the contribution info
        response = app.get(url_resource(contribution_id))
        self.assertEqual(response.json['user_id'], user_id)

        # get the contribution collection
        response = app.get(url_collection)
        self.assertEqual(response.json.get('count'), 1)

        # delete a contribution
        response = app.delete(url_resource(contribution_id))
        response = app.get(url_collection)
        self.assertEqual(response.json.get('count'), 0)
