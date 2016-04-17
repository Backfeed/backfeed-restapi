"""Main entry point
"""
import os

__author__ = 'Jelle Gerbrandy'
__email__ = 'jelle@gerbrandy.com'
__version__ = '0.1'


def main(global_config, **settings):
    from pyramid.config import Configurator
    from backfeed_protocol import utils
    # define the database connection
    sqlite_db = settings.get('sqlite_db')
    if not sqlite_db:
        raise Exception('please specify the sqlite_db setting')
    # utils.init_database(sqlite_db)
    database = utils.init_database(sqlite_db)

    if sqlite_db != ':memory:':
        # create the database file if it does not exists
        if not os.path.exists(sqlite_db):
            utils.setup_database(sqlite_db)
        try:
            database.connect()
        except Exception as error:
            msg = 'Error connecting to {sqlite_db}'.format(sqlite_db=sqlite_db)
            msg += unicode(error)
            raise Exception(msg)

    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("restapi.views")
    config.scan("restapi.views.contributions")
    config.scan("restapi.views.users")
    config.scan("restapi.views.evaluations")
    return config.make_wsgi_app()
