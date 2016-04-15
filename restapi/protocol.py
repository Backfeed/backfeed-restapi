import backfeed_protocol
from backfeed_protocol import utils


def setup_database(sqlite_file=None):
    """set up the database - i.e. create all tables"""
    return utils.setup_database(sqlite_file=sqlite_file)


def reset_database():
    """use with care - removes all data"""
    return utils.reset_database()


def get_contract(contract):
    return backfeed_protocol.get_contract(contract)
