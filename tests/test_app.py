import puppetanalytics.app

def test_main(app, session):
    rv = app.test_client().get('/')
    assert rv.status_code == 200
