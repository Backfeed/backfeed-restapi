import pyramid.httpexceptions as exc
from cornice import Service
from colander import SchemaNode, Float, Integer

import config
from utils import get_contract
from utils import StrictMappingSchema

user_collection_service = Service(name='User Collection', path=config.URL_USER_COLLECTION, description="Users")
user_resource_service = Service(name='User Resource', path=config.URL_USER_RESOURCE, description="Users")


class UserQuerySchema(StrictMappingSchema):
    pass


@user_collection_service.get(validators=(get_contract,), schema=UserQuerySchema)
def collection_get(request):
    """Get a list of users"""
    users = request.contract.get_users()
    return {
        'count': len(users),
        '_meta': {
            'total': request.contract.get_users_count(),
            # 'limit': request.validated['limit'],
            'start': 0,
        },
        'items': [user_to_dict(user) for user in users],
    }


class UserSchema(StrictMappingSchema):
    reputation = SchemaNode(Float(), location='body', type='float', missing=None)
    tokens = SchemaNode(Float(), location='body', type='float', missing=None)
    referrer_id = SchemaNode(Integer(), location='body', type='int', missing=None)


@user_collection_service.post(validators=(get_contract,), schema=UserSchema)
def collection_post(request):
    """Create a new user.
    """
    try:
        user = request.contract.create_user(**request.validated)
    except ValueError as error:
        request.errors.add('query', 'value error', unicode(error))
        return
    return user_to_dict(user)


@user_resource_service.get(validators=(get_contract,))
def get(request):
    """Get the user identified by ``id``"""
    user_id = request.matchdict['id']
    user = request.contract.get_user(user_id)
    if not user:
        raise exc.HTTPNotFound()
    return user_to_dict(user)


def user_to_dict(user):
    """returns a dictionary with information about the user"""
    result = {
        'id': user.id,
        'tokens': float(user.tokens),
        'reputation': user.reputation,
        'reputation_normalized': user.relative_reputation(),
        'total_reputation': user.contract.total_reputation(),
    }
    if user.referrer:
        result['referrer'] = {}
        result['referrer']['id'] = user.referrer.id
    return result
