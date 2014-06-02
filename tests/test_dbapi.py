from puppetanalytics.dbapi import get_author_by_name, insert_raw_deployment


def test_insert_raw_deployment(session, author_joe):
    insert_raw_deployment(session, 'newauthor', 'newmodule',
                          ['tag1', 'tag2'], 0)


def test_insert_raw_deployment_dup_author(session, author_joe):
    insert_raw_deployment(session, 'joe', 'newmodule',
                          ['tag1', 'tag2'], 0)
