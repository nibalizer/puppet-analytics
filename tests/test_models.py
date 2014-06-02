import pytest
from sqlalchemy.exc import IntegrityError

from puppetanalytics.models import Author


def test_author_add(session):
    session.add(Author('joe'))
    session.commit()


def test_author_add_duplicate(session):
    session.add(Author('joe'))
    session.commit()

    session.add(Author('joe'))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
