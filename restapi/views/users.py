from cornice import Service

import config
from utils import get_contract

user_collection_service = Service(name='User Collection', path=config.URL_USER_COLLECTION, description="Users")
user_resource_service = Service(name='User Resource', path=config.URL_USER_RESOURCE, description="Users")


@user_collection_service.get(validators=(get_contract,))
def collection_get(request):
    """Get a list of users"""
    users = request.contract.get_users()
    return {
        'count': len(users),
        'items': [user_to_dict(user) for user in users],
    }


@user_collection_service.post(validators=(get_contract,))
def collection_post(request):
    """Create a *new user*

    :param tokens: the amount of tokens to assign to this user. Must be an integer or a float (like 3.14)

    :param reputation: the amount of reputation to assign to this user. Must be an integer or a float (like 3.14)

    """
    user = request.contract.create_user(**request.POST)
    return user_to_dict(user)


@user_resource_service.get(validators=(get_contract,))
def get(request):
    """Get the user"""
    user_id = request.matchdict['id']
    user = request.contract.get_user(user_id)
    return user_to_dict(user)


def user_to_dict(user):
    """return a dictionary with information about this user"""
    return {
        'id': user.id,
        'tokens': float(user.tokens),
        'reputation': user.relative_reputation(),
    }
