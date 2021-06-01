from flask import current_app

from project.elastic_service.service import ElasticService
from project.elastic_service.indices import EventIndex


class StatsService:
    @staticmethod
    def get_activity_by_email(email: str):
        ElasticService.hosts = [current_app.config.get('ELASTIC_URL_READ')]
        index = EventIndex()
        index.set_index('events_*')
        body = {
            "size":100,
            "query":{
                "bool":{
                    "filter": { 
                        "term": {
                            "email.keyword": email
                        }
                    }
                }
            }
        }
        print(body)
        rsp = ElasticService.search(
            index=index,
            body=body
        )
        print(rsp)
        return rsp
        