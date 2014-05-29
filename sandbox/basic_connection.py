
from datetime import datetime
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()

# datetimes will be serialized
es.index(index="my-index", doc_type="test-type", id=43, body={"any": "data", "timestamp": datetime.now()})
{u'_id': u'43', u'_index': u'my-index', u'_type': u'test-type', u'_version': 1, u'ok': True}

# but not deserialized
print es.get(index="my-index", doc_type="test-type", id=43)['_source']


#{u'any': u'data', u'timestamp': u'2013-05-12T19:45:31.804229'}
