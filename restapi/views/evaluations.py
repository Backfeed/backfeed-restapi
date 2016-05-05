import pyramid.httpexceptions as exc
from cornice import Service

import config
from utils import get_contract
from colander import MappingSchema, SchemaNode, Float, Integer
from utils import StrictMappingSchema
from users import user_to_dict

evaluation_collection_service = Service(name='Evaluation Collection', path=config.URL_EVALUATION_COLLECTION, description="Evaluations")
evaluation_resource_service = Service(name='Evaluation Resource', path=config.URL_EVALUATION_RESOURCE, description="Evaluations")


class EvaluationQuerySchema(StrictMappingSchema):
    contribution_id = SchemaNode(Integer(), location='querystring', type='int', missing=None)
    evaluator_id = SchemaNode(Integer(), location='querystring', type='int', missing=None)


@evaluation_collection_service.get(validators=(get_contract,), schema=EvaluationQuerySchema)
def collection_get(request):
    """Get a list of users"""
    evaluations = request.contract.get_evaluations(**request.validated)
    return {
        'count': len(evaluations),
        'items': [evaluation_to_dict(evaluation, request) for evaluation in evaluations],
    }


class EvaluationSchema(MappingSchema):
    value = SchemaNode(Float(), location='body', type='int')
    evaluator_id = SchemaNode(Integer(), location='body', type='int')
    contribution_id = SchemaNode(Integer(), location='body', type='int')


@evaluation_collection_service.post(validators=(get_contract,), schema=EvaluationSchema)
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
    user = request.contract.get_user(request.validated['evaluator_id'])
    contribution = request.contract.get_contribution(request.validated['contribution_id'])
    value = request.validated['value']
    try:
        evaluation = request.contract.create_evaluation(
            user=user,
            contribution=contribution,
            value=value,
        )
    except ValueError as error:
        request.errors.add('query', 'value error', unicode(error))
        return
    return evaluation_to_dict(evaluation, request)


@evaluation_resource_service.get(validators=(get_contract,))
def get(request):
    """Get evaluations from the contract

    """
    evaluation_id = request.matchdict['id']
    evaluation = request.contract.get_evaluation(evaluation_id)
    if not evaluation:
        raise exc.HTTPNotFound()
    return evaluation_to_dict(evaluation, request)


def evaluation_to_dict(evaluation, request):
    """return a dictionary with information about this evaluation"""
    contribution = evaluation.contribution
    evaluator = evaluation.user
    return {
        'id': evaluation.id,
        'evaluator': user_to_dict(evaluator),
        'contribution': {
            'id': contribution.id,
            'score': request.contract.contribution_score(contribution),
            'engaged_reputation': contribution.engaged_reputation_normal(),
        },
        'value': float(evaluation.value),
    }
