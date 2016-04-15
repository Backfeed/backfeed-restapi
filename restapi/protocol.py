import backfeed_protocol
from backfeed_protocol import utils

SQLITE_FILE = '/tmp/mydatabase.db'


def setup_database(sqlite_file=None):
    if not sqlite_file:
        sqlite_file = SQLITE_FILE
    return utils.setup_database(sqlite_file=sqlite_file)


def reset_database():
    """use with care!"""
    return utils.reset_database()


def get_contract(contract):
    return backfeed_protocol.get_contract(contract)
