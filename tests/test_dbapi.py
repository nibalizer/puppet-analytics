from datetime import datetime

from puppetanalytics.dbapi import (get_all_deployments,
                                   insert_raw_deployment)


def test_get_all_deploymens(session, deployment_1):
    deps = get_all_deployments(session)
    assert len(deps) == 1
    assert deps[0].author.id == deployment_1.author.id


def test_insert_raw_deployment(session):
    now = datetime.now()
    d = insert_raw_deployment(session, 'joe', 'newmodule',
                              ['tag1', 'tag2'], now)
    assert d.author.name == 'joe'
    assert set([x.value for x in d.tags]) == set(['tag1', 'tag2'])


def test_insert_raw_deployment_dup_author(session, author_joe):
    d = insert_raw_deployment(session, 'joe', 'newmodule',
                              ['tag1', 'tag2'], datetime.now())
    assert d.author.name == 'joe'
    assert set([x.value for x in d.tags]) == set(['tag1', 'tag2'])


def test_insert_raw_deployment_dup_tag(session, tag_1):
    d = insert_raw_deployment(session, 'joe', 'newmodule',
                              ['tag1', 'tag2'], datetime.now())
    assert d.author.name == 'joe'
    assert set([x.value for x in d.tags]) == set(['tag1', 'tag2'])
