
from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask

es = Elasticsearch()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello and welcome to Puppet analytics!"

@app.route("/add_dummy")
def add_dummy():
    """
    Add a dummy module download every time this is hit
    """

    doc = {
        'author': 'nibz',
        'name'  : 'puppetboard',
        'tags' : ['awesome', 'ci', 'production'],
        'timestamp': datetime.now(),
    }
    res = es.index(index="module-downloads", doc_type='modules', body=doc)
    return str(res['created'])

@app.route("/list_events")
def list_events():
    """
    Do a massive search to find all module install events
    You probably never want to actually run this
    """
    res = es.search(index="module-downloads", body={"query": {"match_all": {}}})
    response = "<html><body>"
    response += "<p>Got %d Hits:" % res['hits']['total']
    for hit in res['hits']['hits']:
        response += "<p>%(timestamp)s %(author)s: %(name)s %(tags)s" % hit["_source"]
    response += "</body></html>"
    return response

if __name__ == "__main__":
    app.debug = True
    app.run()
