"""Main entry point
"""
__author__ = 'Jelle Gerbrandy'
__email__ = 'jelle@gerbrandy.com'
__version__ = '0.1'


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session


def main(global_config, **settings):
    from pyramid.config import Configurator
    from sqlalchemy import engine_from_config
    from sqlalchemy.orm import sessionmaker

    config = Configurator(settings=settings)
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)
# def main(global_config, **settings):
#     from pyramid.config import Configurator
#     from backfeed_protocol import utils
#     # define the database connection
#     sqlite_db = settings.get('sqlite_db')
#     if not sqlite_db:
#         raise Exception('please specify the sqlite_db setting')
#     # utils.init_database(sqlite_db)
#     database = utils.init_database(sqlite_db)

#     if sqlite_db != ':memory:':
#         # create the database file if it does not exists
#         if not os.path.exists(sqlite_db):
#             utils.setup_database(sqlite_db)
#         try:
#             database.connect()
#         except Exception as error:
#             msg = 'Error connecting to {sqlite_db}'.format(sqlite_db=sqlite_db)
#             msg += unicode(error)
#             raise Exception(msg)

    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("restapi.views")
    config.scan("restapi.views.contributions")
    config.scan("restapi.views.users")
    config.scan("restapi.views.evaluations")
    return config.make_wsgi_app()
