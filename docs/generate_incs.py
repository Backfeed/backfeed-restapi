import os
import json

from restapi.tests import test_users, test_contributions, test_evaluations


class UserInfo(test_users.TestUsers):
    def runTest(self):
        pass

    def user_json(self):
        self.setUp()
        user = self.contract.create_user()
        response = self.app.get(self.url_resource(user.id))
        fn = os.path.join(inc_dir, 'user_json.inc')
        f = open(fn, 'w')
        s = json.dumps(response.json, sort_keys=True, indent=4)
        f.write(s)


class ContributionInfo(test_contributions.TestContributions):
    def runTest(self):
        pass

    def contribution_json(self):
        self.setUp()
        user = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        response = self.app.get(self.url_resource(contribution.id))
        fn = os.path.join(inc_dir, 'contribution_json.inc')
        f = open(fn, 'w')
        s = json.dumps(response.json, sort_keys=True, indent=4)
        f.write(s)


class EvaluationInfo(test_evaluations.TestEvaluations):
    def runTest(self):
        pass

    def evaluation_json(self):
        self.setUp()
        user = self.contract.create_user()
        evaluator = self.contract.create_user()
        contribution = self.contract.create_contribution(user=user)
        evaluation = self.contract.create_evaluation(contribution=contribution, user=evaluator, value=1)
        response = self.app.get(self.url_resource(evaluation.id))
        fn = os.path.join(inc_dir, 'evaluation_json.inc')
        f = open(fn, 'w')
        s = json.dumps(response.json, sort_keys=True, indent=4)
        f.write(s)


inc_dir = os.path.join(os.path.dirname(__file__), 'inc')


def generate_incs():
    UserInfo().user_json()
    ContributionInfo().contribution_json()
    EvaluationInfo().evaluation_json()

if __name__ == '__main__':
    generate_incs()
