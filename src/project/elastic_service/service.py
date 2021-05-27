from elasticsearch import Elasticsearch

class ElasticService:

    client = None
    hosts = None
    
    @staticmethod 
    def get_client():
        if not ElasticService.client:
            ElasticService.client = Elasticsearch(ElasticService.hosts)
        return ElasticService.client

    @staticmethod 
    def delete_index(index):
        client = ElasticService.get_client()
        body = {
            "mappings":index.mapping()            
        }
        res = client.indices.delete(index=index.index, ignore=[400, 404])
        return res

    @staticmethod 
    def create_index(index):
        client = ElasticService.get_client()

        body = {
            "mappings":index.mapping(),
            "settings":{
                "analysis":index.analysis()
            }
        }
        res = client.indices.create(index=index.index, body=body, ignore=400)
        return res
        
    def add_to_index(index, id, object):
        client = ElasticService.get_client()
        res = client.index(index=index.index, doc_type=index.doc_type, id=id, body=object)
        return res

    def delete_from_index(index, id):
        client = ElasticService.get_client()
        res = client.delete(index=index.index, doc_type=index.doc_type, id=id)
        return res

    def search(index, body):
        client = ElasticService.get_client()
        res = client.search(index=index.index, doc_type=index.doc_type, body=body, ignore=400)
        if 'hits' in res and 'hits' in res['hits'] and res['hits']['hits']:
            rsp = []
            for item in res['hits']['hits']:
                i = item['_source']
                i['_score'] = item['_score']
                if 'sort' in item:
                    i['_sort'] = item['sort']
                rsp.append(i)
            return rsp
        else:
            return []

    def get(index, id):
        client = ElasticService.get_client()
        
        try:
            res = client.get(index=index.index, doc_type=index.doc_type, id=id)
        except:
            return None
        
        if res:
            return res['_source']
        else:
            return None
        
        