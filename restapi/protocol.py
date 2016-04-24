import backfeed_protocol
from backfeed_protocol import utils


def reset_database():
    """use with care - removes all data"""
    return utils.reset_database()


def get_contract(contract):
    return backfeed_protocol.utils.get_contract(contract)
