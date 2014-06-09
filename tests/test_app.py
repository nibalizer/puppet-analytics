def test_main(app, session):
    rv = app.test_client().get('/')
    assert rv.status_code == 200


def test_module_page_notfound(app, session):
    rv = app.test_client().get('/nonexistent/foo')
    assert rv.status_code == 404


def test_module_page_joe_notfound(app, session, author_joe):
    rv = app.test_client().get('/joe/foo')
    assert rv.status_code == 404


def test_module_page_one_deployment(app, session, deployment_1):
    rv = app.test_client().get('/joe/module_a')
    assert rv.status_code == 200


def test_module_page_multiple_deployments(app,
                                          session,
                                          deployment_1,
                                          deployment_2):
    rv = app.test_client().get('/joe/module_a')
    assert rv.status_code == 200
