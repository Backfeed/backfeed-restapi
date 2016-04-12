from cornice.resource import resource, view
import protocol


@resource(collection_path='/{contract}/users', path='/{contract}/users/{id}')
class User(object):

    def __init__(self, request):
        self.request = request
        contract_name = self.request.matchdict['contract']
        self.contract = protocol.get_contract(contract_name)

    def collection_get(self):
        """Get a list of users"""
        users = self.contract.get_users()
        return {
            'count': len(users),
            'items': [self.user_to_dict(user) for user in users],
        }

    @view(renderer='json')
    def collection_post(self):
        """Create a *new user*

        :param tokens: the amount of tokens to assign to this user. Must be an integer or a float (like 3.14)

        :param reputation: the amount of reputation to assign to this user. Must be an integer or a float (like 3.14)

        user
        """
        user = self.contract.create_user(**self.request.POST)
        return self.user_to_dict(user)

    @view(renderer='json')
    def get(self):
        """Get the user"""
        user_id = self.request.matchdict['id']
        user = self.contract.get_user(user_id)
        return self.user_to_dict(user)

    @view(renderer='json')
    def put(self):
        """update information of this user"""
        user_id = self.request.matchdict['id']
        user = self.contract.update_user(user_id=user_id, **self.request.POST)
        return self.user_to_dict(user)

    @view()
    def delete(self):
        """Delete this user"""
        user_id = self.request.matchdict['id']
        self.contract.delete_user(user_id)

    @staticmethod
    def user_to_dict(user):
        """return a dictionary with information about this user"""
        return {
            'id': user.id,
            'tokens': float(user.tokens),
            'repuation': float(user.reputation),
        }
