class Index:
    def set_index(self, index_name):
        self.index = index_name
    def mapping(self):
        return {
            self.doc_type:{
                "properties":self.properties()
            }    
        }

    def analysis(self):
        return {
            'filter':{
                'spanish_stop':{
                    'type':'stop',
                    'stopwords':'_spanish_',
                },
                'spanish_stemmer':{
                    'type':'stemmer',
                    'language':'light_spanish'
                }
            },
            'analyzer':{
                'default':{
                    'tokenizer':'standard',
                    'filter':[
                        'lowercase', 
                        'asciifolding', 
                        'spanish_stemmer', 
                        'spanish_stop'
                    ]
                }
            }
        }
    

class EventIndex(Index):

    index = "events"
    doc_type = "doc"

    def properties(self):
        props = {   
            "id": { "type": "integer" },
            "email": { "type": "keyword" },
        }

        return props

