
from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask, request

es = Elasticsearch()
app = Flask(__name__)

@app.route("/")
def hello():
    #res = es.search(index="module-downloads", body={"query": {"match_all": {}},
    #"_source" : ["author", "name"]
    #})
    res = es.search(index="module-downloads", body= {
    "size": "0",
    "aggs": {
        "group_by_author": {
            "terms": {
                "field": "author"
                },
            "aggs": {
                "group_by_name": {
                    "terms": {
                        "field": "name"
                        }
                    }
                }
            }
        }
    })

    response = "<html><body>"
    response = "<p>Hello and welcome to Puppet Analytics!"
    response += "<p>Found %d total module downloads" % res['hits']['total']
    response += "<p>Found %d Authors" % len(res['aggregations']['group_by_author']['buckets'])

    # I feel really stupid doing it this way, isn't there a good way?
    modules_by_author = [ len(i['group_by_name']['buckets']) for i in res['aggregations']['group_by_author']['buckets'] ]
    num_modules = sum(modules_by_author)
    response += " and %d Modules" % num_modules

    response += "</body></html>"
    return response

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

@app.route("/api/1/module_send", methods=['POST'])
def recieve_data():
    data = request.json
    doc = {
        'author': data['author'],
        'name'  : data['name'],
        'tags' : data['tags'].split(),
        'timestamp': datetime.now(),
    }
    res = es.index(index="module-downloads", doc_type='modules', body=doc)
    return str(res['created'])

if __name__ == "__main__":
    app.debug = True
    app.run()
