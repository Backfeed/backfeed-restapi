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
    from backfeed_protocol.models import initialize_sql

    config = Configurator(settings=settings)
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    initialize_sql(engine)

    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)

    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("restapi.views")
    config.scan("restapi.views.contributions")
    config.scan("restapi.views.users")
    config.scan("restapi.views.evaluations")
    return config.make_wsgi_app()
