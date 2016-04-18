from restapi import protocol


def get_contract(request):
    contract_name = request.matchdict['contract']
    request.contract = protocol.get_contract(contract_name)
