from entrypoint import app


def test_hello():
    tester = app.test_client()
    response = tester.get('/test')
    assert response.status_code == 200
