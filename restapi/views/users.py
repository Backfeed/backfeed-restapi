from cornice import Service

import protocol

users_service = Service(name='users', path='/{contract}/users', description="Users Collection")
user_service = Service(name='user', path='/{contract}/users/{user_id}', description="User")


def user_to_dict(user):
    """return a dictionary with information about this user"""
    return {
        'id': user.id,
        'tokens': float(user.tokens),
        'repuation': float(user.reputation),
    }


@users_service.get()
def get_users(request):
    """Returns a list of users"""
    # get the contract
    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)

    users = contract.get_users()
    return {
        'count': len(users),
        'items': [user_to_dict(user) for user in users],
    }


@users_service.post()
def create_user(request):
    """Create a new user
    """
    # get the contract
    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)

    user = contract.create_user(**request.POST)
    return user_to_dict(user)


@user_service.get()
def get_user(request):
    """return the user identified by `user_id`
    """
    user_id = request.matchdict['user_id']
    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)
    user = contract.get_user(user_id)
    return user_to_dict(user)


@user_service.put()
def update_user(request):
    """update the user information"""
    user_id = request.matchdict['user_id']

    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)
    user = contract.update_user(user_id=user_id, **request.POST)
    return user_to_dict(user)


@user_service.delete()
def delete_user(request):
    """update the user information"""
    user_id = request.matchdict['user_id']
    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)
    contract.delete_user(user_id)
