from restapi import protocol
from colander import MappingSchema, Mapping


def get_contract(request):
    contract_name = request.matchdict['contract']
    request.contract = protocol.get_contract(contract_name)


class StrictMappingSchema(MappingSchema):
    def schema_type(self, **kw):
        return Mapping(unknown='raise')
