import datetime
import os
import requests

from flask import (abort,
                   Flask,
                   request,
                   make_response,
                   render_template)

import db
from dbapi import (get_all_authors_count,
                   get_all_deployments,
                   get_all_deployments_count,
                   get_all_module_author_combination_count,
                   get_deploys_by_author_module_after_date,
                   get_deployment_count_for_all_author_modules,
                   insert_raw_deployment)

app = Flask(__name__)


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


@app.route("/shields/<author>/<module>/<days>")
def downloads_shield(author, module, days):
    """
    Return download count shield
    """

    days = int(days)

    now = datetime.datetime.utcnow()
    today_begins = datetime.datetime(now.year, now.month, now.day)
    start_date = today_begins - datetime.timedelta(days=days)

    deployments = get_deploys_by_author_module_after_date(db.Session(),
                                                          author,
                                                          module,
                                                          start_date)

    count = len(deployments)
    if days == 7:
        period = "week"
    elif 28 < days < 31:
        period = "month"
    else:
        period = "last {0} days".format(days)

    r = requests.get(("http://img.shields.io/badge/downloads-"
                      "{0}/{1}"
                      "-brightgreen.svg").format(count, period))

    if r.ok is True:
        response = make_response(r.content)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        response.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'

        return response
    else:
        return ""


@app.route("/<author>/<module>")
def module_page(author, module):
    """
    Page to display a modules stats/data
    """

    now = datetime.datetime.utcnow()
    today_begins = datetime.datetime(now.year, now.month, now.day)
    start_date = today_begins - datetime.timedelta(days=7)

    deployments = get_deploys_by_author_module_after_date(db.Session(),
                                                          author,
                                                          module,
                                                          start_date)

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

    day = datetime.timedelta(days=1)

    # Build bucket_number range of times
    # initialize x values with zero
    for i in range(bucket_number + 1):
        ys.append(0)
        t = now - (day * (bucket_number - i))
        xs.append(int(t.strftime('%s')))

    # Put each deploy into a bucket
    day_num = 0
    moving_date = today_begins
    # Pop deploys off, earliest first
    for deploy in module_deploys:
        Success = False
        while not Success:
            if deploy['timestamp'] > moving_date:
                ys[-1 * (day_num + 1)] += 1
                Success = True
            else:
                day_num += 1
                moving_date -= day

    return render_template('module.html',
                           xs=xs,
                           ys=ys,
                           author=author,
                           modulename=module,
                           hits=len(module_deploys),
                           module_deploys=module_deploys)


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
    insert_raw_deployment(db.Session(),
                          author,
                          module,
                          tags,
                          datetime.datetime.utcnow())
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
