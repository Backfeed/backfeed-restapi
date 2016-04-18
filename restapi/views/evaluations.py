from cornice.resource import resource, view
from .. import protocol


@resource(collection_path='/{contract}/evaluations', path='/{contract}/evaluations/{id}')
class User(object):

    def __init__(self, request):
        self.request = request
        contract_name = self.request.matchdict['contract']
        self.contract = protocol.get_contract(contract_name)

    @view(renderer='json')
    def collection_get(self):
        """Get a list of evaluations"""
        evaluations = self.contract.get_evaluations()
        return {
            'count': len(evaluations),
            'items': [self.to_dict(evaluation) for evaluation in evaluations],
        }

    @view(renderer='json')
    def collection_post(self):
        """Create a new evaluation

        :param user_id: required
        :param contribution_id: required
        :param value: required
        """
        user = self.contract.get_user(self.request.POST['user_id'])
        contribution = self.contract.get_contribution(self.request.POST['contribution_id'])
        value = self.request.POST['value']
        evaluation = self.contract.create_evaluation(
            user=user,
            contribution=contribution,
            value=value,
        )
        return self.to_dict(evaluation)

    @view(renderer='json')
    def get(self):
        """Get the evaluation"""
        evaluation_id = self.request.matchdict['id']
        evaluation = self.contract.get_evaluation(evaluation_id)
        return self.to_dict(evaluation)

    # @view(renderer='json')
    # def put(self):
    #     """Update information of this user"""
    #     evaluation_id = self.request.matchdict['id']
    #     evaluation = self.contract.update_evaluation(evaluation_id=evaluation_id, **self.request.POST)
    #     return self.to_dict(evaluation)
    #
    # @view()
    # def delete(self):
    #     """Delete this evaluation"""
    #     evaluation_id = self.request.matchdict['id']
    #     self.contract.delete_evaluation(evaluation_id)

    def to_dict(self, evaluation):
        """return a dictionary with information about this evaluation"""
        contribution = evaluation.contribution
        evaluator = evaluation.user
        return {
            'id': evaluation.id,
            'evaluator': {
                'id': evaluator.id,
                'tokens': evaluator.tokens,
                'reputation': evaluator.relative_reputation(),
            },
            'contribution': {
                'id': contribution.id,
                'score': self.contract.contribution_score(contribution),
                'engaged_reputation': contribution.engaged_reputation(),
            },
            'value': float(evaluation.value),
        }
