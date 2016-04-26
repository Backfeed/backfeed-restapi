from cornice import Service

import config
from utils import get_contract


contribution_collection_service = Service(name='Contribution Collection', path=config.URL_CONTRIBUTION_COLLECTION, description="Contributions")
contribution_resource_service = Service(name='Contribution Resource', path=config.URL_CONTRIBUTION_RESOURCE, description="Contributions")


@contribution_collection_service.get(validators=(get_contract,))
def collection_get(request):
        """Get a list of contributions"""
        contributions = request.contract.get_contributions()
        return {
            'count': len(contributions),
            'items': [contribution_to_dict(contribution, request) for contribution in contributions],
        }


@contribution_collection_service.post(validators=(get_contract,))
def collection_post(request):
    """Create a new contribution

    :param contributor_id:
        the id of the user that has made the contribution

    :returns: information about the new contribution
    """
    user_id = request.POST['contributor_id']
    user = request.contract.get_user(user_id)
    contribution = request.contract.create_contribution(user=user)
    return contribution_to_dict(contribution, request)


@contribution_resource_service.get(validators=(get_contract,))
def get(request):
    """Get the contribution"""
    contribution_id = request.matchdict['id']
    contribution = request.contract.get_contribution(contribution_id)
    return contribution_to_dict(contribution, request)


def contribution_to_dict(contribution, request):
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
        'contributor': {
            'id': user.id,
            'tokens': user.tokens,
            'reputation': user.relative_reputation(),
        },
        'type': contribution.contribution_type,
        'stats': stats,
    }
