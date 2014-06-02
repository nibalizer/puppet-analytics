from datetime import datetime

from puppetanalytics.dbapi import insert_raw_deployment


def test_insert_raw_deployment(session):
    insert_raw_deployment(session, 'newauthor', 'newmodule',
                          ['tag1', 'tag2'], datetime.now())


def test_insert_raw_deployment_dup_author(session, author_joe):
    insert_raw_deployment(session, 'joe', 'newmodule',
                          ['tag1', 'tag2'], datetime.now())


def test_insert_raw_deployment_dup_tag(session, tag_1):
    insert_raw_deployment(session, 'newauthor', 'newmodule',
                          ['tag1', 'tag2'], datetime.now())
