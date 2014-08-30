import datetime
import os

from flask import (abort,
                   Flask,
                   request,
                   render_template)

import db
from dbapi import (get_all_authors_count,
                   get_all_deployments,
                   get_all_deployments_count,
                   get_all_module_author_combination_count,
                   get_deployments_by_author_module,
                   get_deployment_count_for_all_author_modules,
                   insert_raw_deployment)

app = Flask(__name__)


def divtd(td1, td2):
    us1 = td1.microseconds + 1000000 * (td1.seconds + 86400 * td1.days)
    us2 = td2.microseconds + 1000000 * (td2.seconds + 86400 * td2.days)
    return us1 / us2


@app.route("/")
def mainpage():
    """
    Main page to display some summary stats
    """
    session = db.Session()
    aggregates = get_deployment_count_for_all_author_modules(session)
    total_authors = get_all_authors_count(session)
    total_downloads = get_all_deployments_count(session)
    total_modules = get_all_module_author_combination_count(session)
    aggregates = [(agg[0],
                   agg[1].author.name,
                   agg[1].module.name) for agg in aggregates]

    return render_template('mainpage.html',
                           total_downloads=total_downloads,
                           total_authors=total_authors,
                           total_modules=total_modules,
                           deploy_aggregates=aggregates)


@app.route("/<author>/<module>")
def module_page(author, module):
    """
    Page to display a modules stats/data
    """
    deployments = get_deployments_by_author_module(db.Session(),
                                                   author,
                                                   module)

    if len(deployments) == 0:
        return abort(404)

    module_deploys = []
    for deployment in deployments:
        module_deploys.append({
            'timestamp': deployment.occured_at,
            'author': deployment.author.name,
            'name': deployment.module.name,
            'tags': [x.value for x in deployment.tags]
        })

    # Divide all deploys into 7 24 hour buckets, send to c3.js

    # Theoretically can change graphing window to be anything
    bucket_number = 7

    # The x/y values we will return
    # X values are the unix seconds of the start of the day
    # Y values are number of deploys on the day
    xs = []
    ys = []

    now = datetime.datetime.utcnow()

    day = datetime.timedelta(days=1)

    # Build bucket_number range of times
    # initialize x values with zero
    for i in range(bucket_number):
        ys.append(0)
        t = now - (day * (i + 1))
        xs.append(int(t.strftime('%s')))

    # We dont want any deploys before this time
    cutoff_time = now - (day * bucket_number)

    # Put each deploy into a bucket using division
    # Custom timedelta divison because
    # timedelta has now __div__
    for deploy in module_deploys:
        if deploy['timestamp'] < cutoff_time:
            continue
        day_num = divtd((deploy['timestamp'] - cutoff_time), day)
        ys[day_num] += 1

    # Finally we reverse the lists so that the graph
    # reads from left to right
    xs = xs[::-1]

    return render_template('module.html',
                           xs=xs,
                           ys=ys,
                           author=author,
                           modulename=module,
                           hits=len(module_deploys),
                           module_downloads=module_deploys)


@app.route("/add_dummy")
def add_dummy():
    """
    Add a dummy module download every time this is hit
    """

    insert_raw_deployment(db.Session(),
                          'nibz',
                          'puppetboard',
                          ['awesome', 'ci', 'production'],
                          datetime.datetime.utcnow())
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
    try:
        author = data['author']
        module = data['name']
    except (KeyError, TypeError):
        abort(400)

    try:
        tags = data['tags']
    except KeyError:
        tags = []
    else:
        tags = tags.split(',')
    try:
        date = datetime.datetime.utcfromtimestamp(float(data['date']))
    except (KeyError):
        date = datetime.datetime.utcnow()
    insert_raw_deployment(db.Session(),
                          author,
                          module,
                          tags,
                          date)
    return 'True'


def init_database():
    db.Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    init_database()
    # Load production settings by default
    app.config.from_object('puppetanalytics.settings.ProductionSettings')
    # Override default settings if PUPPETANALYTICS_SETTINGS is set to class
    # inherited from Settings class, e.g. run development mode with
    # PUPPETANALYTICS_SETTINGS=puppetanalytics.settings.DevelopmentSettings
    if os.environ.get('PUPPETANALYTICS_SETTINGS') is not None:
        app.config.from_object(os.environ['PUPPETANALYTICS_SETTINGS'])
    app.run()
