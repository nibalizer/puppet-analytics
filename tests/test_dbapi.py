from datetime import datetime


from puppetanalytics.dbapi import (get_all_authors_count,
                                   get_all_deployments,
                                   get_all_deployments_count,
                                   get_all_module_author_combination_count,
                                   get_deploys_by_author_module_after_date,
                                   get_deployments_by_module,
                                   insert_raw_deployment)


def test_get_all_authors_count_zero(session):
    assert get_all_authors_count(session) == 0


def test_get_all_authors_count_one(session, author_joe):
    assert get_all_authors_count(session) == 1


def test_get_all_deployments_count_none(session):
    assert get_all_deployments_count(session) == 0


def test_get_all_deployments_count_one(session, deployment_1):
    assert get_all_deployments_count(session) == 1


def test_get_all_module_author_combinations_count(session, deployment_1):
    assert get_all_module_author_combination_count(session) == 1


def test_get_all_deploymens(session, deployment_1):
    deps = get_all_deployments(session)
    assert len(deps) == 1
    assert deps[0].author.id == deployment_1.author.id


def test_get_deployments_by_module(session, deployment_1):
    deps = get_deployments_by_module(session, 'module_a')
    assert len(deps) == 1

    deps = get_deployments_by_module(session, 'nonexistent')
    assert len(deps) == 0


def test_get_deploys_by_author_module_after_date(session,
                                                 deployment_1):
    deps = get_deploys_by_author_module_after_date(session,
                                                   'joe',
                                                   'module_a')
    assert len(deps) == 1

    deps = get_deploys_by_author_module_after_date(session,
                                                   'joe',
                                                   'nonexistent')
    assert len(deps) == 0

    deps = get_deploys_by_author_module_after_date(session,
                                                   'nonexistent',
                                                   'module_a')
    assert len(deps) == 0


def test_insert_raw_deployment(session):
    now = datetime.utcnow()
    d = insert_raw_deployment(session, 'joe', 'newmodule',
                              ['tag1', 'tag2'], now)
    assert d.author.name == 'joe'
    assert set([x.value for x in d.tags]) == set(['tag1', 'tag2'])


def test_insert_raw_deployment_dup_author(session, author_joe):
    d = insert_raw_deployment(session, 'joe', 'newmodule',
                              ['tag1', 'tag2'], datetime.utcnow())
    assert d.author.name == 'joe'
    assert set([x.value for x in d.tags]) == set(['tag1', 'tag2'])


def test_insert_raw_deployment_dup_tag(session, tag_1):
    d = insert_raw_deployment(session, 'joe', 'newmodule',
                              ['tag1', 'tag2'], datetime.utcnow())
    assert d.author.name == 'joe'
    assert set([x.value for x in d.tags]) == set(['tag1', 'tag2'])
