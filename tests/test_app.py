def test_main(app, session):
    rv = app.test_client().get('/')
    assert rv.status_code == 200


def test_module_page_notfound(app, session):
    rv = app.test_client().get('/nonexistent/foo')
    assert rv.status_code == 404


def test_module_page_joe_notfound(app, session, author_joe):
    rv = app.test_client().get('/joe/foo')
    assert rv.status_code == 404


def test_module_page_post(app, session, deployment_1):
    rv = app.test_client().post('/joe/module_a', data={})
    assert rv.status_code == 405


def test_module_page_one_deployment(app, session, deployment_1):
    rv = app.test_client().get('/joe/module_a')
    assert rv.status_code == 200


def test_module_page_multiple_deployments(app,
                                          session,
                                          deployment_1,
                                          deployment_2):
    rv = app.test_client().get('/joe/module_a')
    assert rv.status_code == 200


def test_module_page_and_graph_multiple_deployments(app,
                                                    session,
                                                    deployment_1,
                                                    deployment_2):
    rv = app.test_client().get('/joe/module_a')
    # Verify it is attempting to create a graph
    assert str(rv.data).find('createDeployTrendsGraph') != -1
    # Verify the graph is given the right inputs
    assert str(rv.data).find('[0, 0, 0, 0, 0, 0, 0, 2]') != -1
    # This obviously isn't perfect, but much better than nothing


def test_graph_relative_time(app,
                             session,
                             deployment_3):
    rv = app.test_client().get('/joe/module_a')
    # Verify it is attempting to create a graph
    assert str(rv.data).find('createDeployTrendsGraph') != -1
    # Verify the graph is given the right inputs
    assert str(rv.data).find('[0, 0, 0, 0, 0, 0, 1, 0]') != -1
    # This is better than the above test because the deployment
    # Time in deploy 3 is set to be 24 hrs before. So if the graph
    # Comes out looking like this ^^ we're in pretty good shape
