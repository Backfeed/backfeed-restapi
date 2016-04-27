from cornice import Service
from backfeed_protocol.models import Base

info_service = Service(name='Info', path='/_info', description="Info")


@info_service.get()
def get_info(request):
    """return some general configuration information"""
    return {
        'engine_url': unicode(Base.metadata.bind.url),
        'settings': request.registry.settings
    }
