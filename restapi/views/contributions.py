from cornice.resource import resource, view
import protocol


@resource(collection_path='/{contract}/contributions', path='/{contract}/contributions/{id}')
class Contributions(object):

    def __init__(self, request):
        self.request = request
        contract_name = self.request.matchdict['contract']
        self.contract = protocol.get_contract(contract_name)

    def collection_get(self):
        """Get a list of contributions"""
        contributions = self.contract.get_contributions()
        return {
            'count': len(contributions),
            'items': [self.to_dict(contribution) for contribution in contributions],
        }

    @view(renderer='json')
    def collection_post(self):
        """Create a new contribution

        :param user_id: required, the id of an user

        :returns: information about the new contributions
        """
        user_id = self.request.POST['user_id']
        user = self.contract.get_user(user_id)
        contribution = self.contract.create_contribution(user=user)
        return self.to_dict(contribution)

    @view(renderer='json')
    def get(self):
        """Get the contribution"""
        contribution_id = self.request.matchdict['id']
        contribution = self.contract.get_contribution(contribution_id)
        return self.to_dict(contribution)

    @view(renderer='json')
    def put(self):
        """Update information of this contribution"""
        contribution_id = self.request.matchdict['id']
        contribution = self.contract.update_contribution(contribution_id=contribution_id, **self.request.POST)
        return self.to_dict(contribution)

    @view()
    def delete(self):
        """Delete this user"""
        contribution_id = self.request.matchdict['id']
        self.contract.delete_contribution(contribution_id)

    @staticmethod
    def to_dict(contribution):
        """return a dictionary with information about this contribution"""
        return {
            'id': contribution.id,
            'user_id': float(contribution.user.id),
        }
