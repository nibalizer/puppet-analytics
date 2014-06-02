from datetime import datetime

from flask import Flask, request, render_template

import db
from dbapi import (get_all_deployments,
                   get_deployments_by_author_module,
                   insert_raw_deployment)

app = Flask(__name__)


@app.route("/")
def mainpage():
    """
    The previous page was silly. Please feel free to make a new one.
    """
    return "Hi"


@app.route("/<author>/<module>")
def module_page(author, module):
    """
    Page to display a modules stats/data
    """
    deployments = get_deployments_by_author_module(db.Session(),
                                                   author,
                                                   module)

    module_downloads = []
    for deployment in deployments:
        module_downloads.append({
            'timestamp': deployment.occured_at,
            'author': deployment.author.name,
            'name': deployment.module.name,
            'tags': [x.value for x in deployment.tags]
        })

    return render_template('module.html',
                           modulename=module,
                           hits=len(module_downloads),
                           module_downloads=module_downloads)


@app.route("/add_dummy")
def add_dummy():
    """
    Add a dummy module download every time this is hit
    """

    insert_raw_deployment(db.Session(),
                          'nibz',
                          'puppetboard',
                          ['awesome', 'ci', 'production'],
                          datetime.now())
    return 'True'


@app.route("/list_events")
def list_events():
    """
    Do a massive search to find all module install events
    You probably never want to actually run this
    """
    deployments = get_all_deployments(db.Session())
    response = "<html><body>"
    response += "<p>Got %d Hits:" % len(deployments)
    for hit in deployments:
        response += "<p>%(timestamp)s %(author)s: %(module)s %(tags)s" % \
            {'timestamp': hit.occured_at,
             'author': hit.author.name,
             'module': hit.module.name,
             'tags': [x.value for x in hit.tags]}
    response += "</body></html>"
    return response


@app.route("/api/1/module_send", methods=['POST'])
def recieve_data():
    data = request.json
    insert_raw_deployment(db.Session(),
                          data['author'],
                          data['name'],
                          data['tags'].split(),
                          datetime.now())
    return 'True'


def init_database():
    db.Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    init_database()
    app.debug = True
    app.run()
