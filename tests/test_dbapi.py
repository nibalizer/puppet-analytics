from datetime import datetime

from puppetanalytics.dbapi import (get_all_deployments,
                                   get_deployments_by_author_module,
                                   get_deployments_by_module,
                                   insert_raw_deployment)


def test_get_all_deploymens(session, deployment_1):
    deps = get_all_deployments(session)
    assert len(deps) == 1
    assert deps[0].author.id == deployment_1.author.id


def test_get_deployments_by_module(session, deployment_1):
    deps = get_deployments_by_module(session, 'module_a')
    assert len(deps) == 1

    deps = get_deployments_by_module(session, 'nonexistent')
    assert len(deps) == 0


def test_get_deployments_by_author_module(session, deployment_1):
    deps = get_deployments_by_author_module(session, 'joe', 'module_a')
    assert len(deps) == 1

    deps = get_deployments_by_author_module(session, 'joe', 'nonexistent')
    assert len(deps) == 0

    deps = get_deployments_by_author_module(session, 'nonexistent', 'module_a')
    assert len(deps) == 0


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
