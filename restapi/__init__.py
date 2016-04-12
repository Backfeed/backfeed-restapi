"""Main entry point
"""
from pyramid.config import Configurator

__author__ = 'Jelle Gerbrandy'
__email__ = 'jelle@gerbrandy.com'
__version__ = '0.1'


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("restapi.views")
    config.scan("restapi.views.users")
    return config.make_wsgi_app()
