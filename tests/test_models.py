import puppetanalytics.db as db


def test_create_all():
    db.Base.metadata.create_all(db.engine)
