import pyramid.httpexceptions as exc
from cornice import Service
from colander import SchemaNode, Integer, String

from backfeed_protocol.contracts.exceptions import InvalidContributionTypeError

import config
from utils import get_contract
from utils import StrictMappingSchema
from users import user_to_dict

contribution_collection_service = Service(name='Contribution Collection', path=config.URL_CONTRIBUTION_COLLECTION, description="Contributions")
contribution_resource_service = Service(name='Contribution Resource', path=config.URL_CONTRIBUTION_RESOURCE, description="Contributions")


class ContributionQuerySchema(StrictMappingSchema):
    contributor_id = SchemaNode(Integer(), location='querystring', type='int', missing=None)
    order_by = SchemaNode(String(), location='querystring', type='str', missing='-score')
    contribution_type = SchemaNode(String(), name='type', location='querystring', type='str', missing=None)

    limit = SchemaNode(Integer(), location='querystring', type='int', missing=100)
    start = SchemaNode(Integer(), location='querystring', type='int', missing=0)


@contribution_collection_service.get(validators=(get_contract,), schema=ContributionQuerySchema)
def collection_get(request):
        """Get a list of contributions.

        The parameter 'order_by' can take as its values:

        - *score* order by score
        - *-score*  order descendingly, by score
        - *time*: the time the contribution was added
        - *-time*: last-added first
        """
        kwargs = request.validated
        kwargs['contribution_type'] = kwargs['type']
        del kwargs['type']
        contributions = request.contract.get_contributions(**kwargs)
        return {
            '_meta': {
                'total': request.contract.contributions_count(**kwargs),
                'limit': request.validated['limit'],
                'start': request.validated['start'],
            },
            'items': [contribution_to_dict(contribution) for contribution in contributions],
        }


class ContributionSchema(StrictMappingSchema):
    contributor_id = SchemaNode(Integer(), location='body', type='int')
    contribution_type = SchemaNode(String(), name='type', location='body', type='str', missing=None)


@contribution_collection_service.post(validators=(get_contract,), schema=ContributionSchema)
def collection_post(request):
    """Create a new contribution
    :returns: information about the new contribution
    """
    user_id = request.validated['contributor_id']
    user = request.contract.get_user(user_id)
    contribution_type = request.validated['type']
    try:
        contribution = request.contract.create_contribution(user=user, contribution_type=contribution_type)
    except InvalidContributionTypeError as error:
        raise exc.HTTPBadRequest(error)
    return contribution_to_dict(contribution)


@contribution_resource_service.get(validators=(get_contract,))
def get(request):
    """Get the contribution"""
    contribution_id = request.matchdict['id']
    contribution = request.contract.get_contribution(contribution_id)
    if not contribution:
        raise exc.HTTPNotFound()
    return contribution_to_dict(contribution)


def contribution_to_dict(contribution):
    """return a dictionary with information about this contribution"""
    user = contribution.user
    stats = contribution.get_statistics()
    # show only normalized values for the reputation fields
    stats['engaged_reputation'] = stats['engaged_reputation_normal']
    del stats['engaged_reputation_normal']
    for val in stats['evaluations']:
        stats['evaluations'][val]['reputation'] = stats['evaluations'][val]['reputation_normal']
        del stats['evaluations'][val]['reputation_normal']

    return {
        'id': contribution.id,
        'contributor': user_to_dict(user),
        'type': contribution.contribution_type,
        'stats': stats,
    }
