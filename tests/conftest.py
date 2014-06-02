from datetime import datetime
import pytest

from puppetanalytics import db as _db
from puppetanalytics.models import Author, Deployment, Module, Tag


@pytest.fixture(scope='function')
def db(request):
    _db.Base.metadata.create_all(_db.engine)

    def teardown():
        _db.Base.metadata.drop_all(_db.engine)

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    db.session = _db.Session()

    def teardown():
        db.session.commit()
        db.session.rollback()

    request.addfinalizer(teardown)
    return db.session


@pytest.fixture(scope='function')
def author_joe(session):
    joe = Author('joe')
    session.add(joe)
    session.commit()
    return joe


@pytest.fixture(scope='function')
def module_a(session):
    m = Module('module_a')
    session.add(m)
    session.commit()
    return m


@pytest.fixture(scope='function')
def tag_1(session):
    tag_1 = Tag('tag_1')
    session.add(tag_1)
    session.commit()
    return tag_1


@pytest.fixture(scope='function')
def deployment_1(session,
                 author_joe,
                 module_a,
                 tag_1):
    d = Deployment(author_joe.id, module_a.id, datetime.now())
    d.tags = [tag_1]
    session.add(d)
    session.commit()
    return d
