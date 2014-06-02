from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template

es = Elasticsearch()
app = Flask(__name__)


@app.route("/")
def mainpage():
    res = es.search(index="module-downloads",
                    body={
                        "size": "0",
                        "aggs": {
                            "group_by_author": {
                                "terms": {"field": "author"},
                                "aggs": {
                                    "group_by_name": {
                                        "terms": {"field": "name"}
                                    }
                                }
                            }
                        }
                    })

    authors = res['aggregations']['group_by_author']['buckets']
    total_downloads = res['hits']['total']
    num_authors = len(authors)

    # I feel really stupid doing it this way, isn't there a good way?
    modules_by_author = [
        len(author['group_by_name']['buckets']) for author in
        res['aggregations']['group_by_author']['buckets']]
    num_modules = sum(modules_by_author)

    author_module = {}

    for author in res['aggregations']['group_by_author']['buckets']:
        author_name = author['key']
        author_module[author_name] = {}
        for module in author['group_by_name']['buckets']:
            module_name = module['key']
            author_module[author_name][module_name] = {
                'events': module['doc_count']}

    return render_template('mainpage.html',
                           total_downloads=total_downloads,
                           num_authors=num_authors,
                           num_modules=num_modules,
                           author_module=author_module)


@app.route("/<author>/<module>")
def module_page(author, module):
    """
    Page to display a modules stats/data
    """
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"name": module}},
                    {"match": {"author": author}}
                ]
            }
        }
    }

    res = es.search(index="module-downloads", body=query)
    hits = res['hits']['total']
    module_downloads = []
    for hit in res['hits']['hits']:
        module_downloads.append({
            'timestamp': "%(timestamp)s" % hit["_source"],
            'author': "%(author)s" % hit["_source"],
            'name': "%(name)s" % hit["_source"],
            'tags': "%(tags)s" % hit["_source"],
        })

    return render_template('module.html',
                           author=author,
                           modulename=module,
                           hits=hits,
                           module_downloads=module_downloads)


@app.route("/add_dummy")
def add_dummy():
    """
    Add a dummy module download every time this is hit
    """

    doc = {
        'author': 'nibz',
        'name': 'puppetboard',
        'tags': ['awesome', 'ci', 'production'],
        'timestamp': datetime.now(),
    }
    res = es.index(index="module-downloads", doc_type='modules', body=doc)
    return str(res['created'])


@app.route("/api/1/module_send", methods=['POST'])
def recieve_data():
    data = request.json
    doc = {
        'author': data['author'],
        'name': data['name'],
        'tags': data['tags'].split(),
        'timestamp': datetime.now(),
    }
    res = es.index(index="module-downloads", doc_type='modules', body=doc)
    return str(res['created'])


if __name__ == "__main__":
    app.debug = True
    app.run()
