from cornice import Service

import config
from utils import get_contract


evaluation_collection_service = Service(name='Evaluation Collection', path=config.URL_EVALUATION_COLLECTION, description="Evaluations")
evaluation_resource_service = Service(name='Evaluation Resource', path=config.URL_EVALUATION_RESOURCE, description="Evaluations")


@evaluation_collection_service.get(validators=(get_contract,))
def collection_get(request):
    """Get a list of users"""
    evaluations = request.contract.get_evaluations()
    return {
        'count': len(evaluations),
        'items': [evaluation_to_dict(evaluation, request) for evaluation in evaluations],
    }


@evaluation_collection_service.post(validators=(get_contract,))
def collection_post(request):
    """Create a new evaluation.

    Creating an evaluation will update tokens and reputation from the contributor,
    the evaluator, and previous evaluators.

    :param evaluator_id:
        required. The id of the user to that does the evaluation.
    :param contribution_id:
        required. The id of the contribution that is being evaluated
    :param value:
        required. This is a number - which values are accepted depends on the contract.


    :returns:
        information about the added evaluation

    """
    user = request.contract.get_user(request.POST['evaluator_id'])
    contribution = request.contract.get_contribution(request.POST['contribution_id'])
    value = request.POST['value']
    evaluation = request.contract.create_evaluation(
        user=user,
        contribution=contribution,
        value=value,
    )
    return evaluation_to_dict(evaluation, request)


@evaluation_resource_service.get(validators=(get_contract,))
def get(request):
    """Get evaluations from the contract

    """
    evaluation_id = request.matchdict['id']
    evaluation = request.contract.get_evaluation(evaluation_id)
    return evaluation_to_dict(evaluation, request)


def evaluation_to_dict(evaluation, request):
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
            'score': request.contract.contribution_score(contribution),
            'engaged_reputation': contribution.engaged_reputation(),
        },
        'value': float(evaluation.value),
    }
