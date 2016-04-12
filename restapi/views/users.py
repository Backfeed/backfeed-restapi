from cornice import Service

import protocol

users_service = Service(name='users', path='/{contract}/users', description="Users Collection")
user_service = Service(name='user', path='/{contract}/users/{user_id}', description="User")


@users_service.get()
def get_users(request):
    """Returns a list of users"""
    # get the contract
    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)

    users = contract.get_users()
    return {
        'count': len(users),
        'items': [user for user in users],
    }


@user_service.get()
def get_user(request):
    """return the user identified by `user_id`
    """
    user_id = request.matchdict['user_id']
    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)
    user = contract.get_user(user_id)
    return {
        'id': user.id,
    }


@user_service.post()
def update_user(request):
    """update the user information"""
    user_id = request.matchdict['user_id']

    contract_name = request.matchdict['contract']
    contract = protocol.get_contract(contract_name)
    user = contract.get_user(user_id)
    return {
        'id': user.id,
    }
