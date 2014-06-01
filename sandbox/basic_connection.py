
from datetime import datetime
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()

# datetimes will be serialized
es.index(index="my-index",
         doc_type="test-type",
         id=43,
         body={"any": "data", "timestamp": datetime.now()})

# but not deserialized
print es.get(index="my-index", doc_type="test-type", id=43)['_source']
