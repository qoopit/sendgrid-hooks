from flask import current_app
from datetime import datetime

from project.elastic_service.service import ElasticService
from project.elastic_service.indices import EventIndex

class SendgridService:
    @staticmethod
    def insert(doc):
        ElasticService.hosts = [current_app.config.get('ELASTIC_URL')]
        index = EventIndex()
        index.set_index('events_{}'.format(datetime.utcnow().strftime('%Y%m%d')))
        ElasticService.create_index(index)
        if 'timestamp' in doc:
            doc['@time'] = datetime.fromtimestamp(doc.get('timestamp'))
        return ElasticService.add_to_index(index, doc.get('sg_event_id', None), doc)
