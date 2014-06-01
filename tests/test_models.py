import pytest
from sqlalchemy.exc import IntegrityError

from puppetanalytics.models import Author
from puppetanalytics import db as _db


@pytest.fixture(scope='function')
def db():
    _db.Base.metadata.drop_all(_db.engine)
    _db.Base.metadata.create_all(_db.engine)
    return _db


def test_create_all(db):
    db.Base.metadata.create_all(db.engine)


def test_author_add(db):
    session = db.Session()
    session.add(Author('joe'))
    session.commit()


def test_author_add_duplicate(db):
    session = db.Session()
    session.add(Author('joe'))
    session.commit()

    session = db.Session()
    session.add(Author('joe'))
    with pytest.raises(IntegrityError):
        session.commit()
