import json
import datetime

from puppetanalytics.dbapi import get_all_deployments


def test_module_send_empty(app):
    rv = app.test_client().post('/api/1/module_send', data={})
    assert rv.status_code == 400


def test_module_send_valid(app, session):
    rv = app.test_client().post('/api/1/module_send', data=json.dumps({
        'author': 'bob',
        'name': 'somemodule',
        'tags': 'tag_foo,tag_bar'}),
        content_type='application/json')
    assert rv.status_code == 200

    deployments = get_all_deployments(session)
    assert deployments[0].author.name == 'bob'
    assert deployments[0].module.name == 'somemodule'
    assert set([x.value for x in deployments[0].tags])\
        == set(['tag_foo', 'tag_bar'])


def test_module_send_date(app, session):
    rv = app.test_client().post('/api/1/module_send', data=json.dumps({
        'author': 'bob',
        'name': 'somemodule',
        'date': '1409339392',
        'tags': 'tag_foo,tag_bar'}),
        content_type='application/json')
    assert rv.status_code == 200

    deployments = get_all_deployments(session)
    assert deployments[0].author.name == 'bob'
    assert deployments[0].module.name == 'somemodule'
    assert deployments[0].occured_at == datetime.datetime(
        2014, 8, 29, 19, 9, 52)
    assert set([x.value for x in deployments[0].tags])\
        == set(['tag_foo', 'tag_bar'])
