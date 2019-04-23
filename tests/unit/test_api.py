import pytest
from core.api import app
access = "doesn't matter"
root = "/config_api/"

@pytest.fixture
def client(mocker):
    flask = app.create_app()
    client = flask.test_client()
    yield client

def test_good_login(client, mocker):
    mocker.patch("core.api.auth.parse_oauth", return_value="njb@integrichain.com")
    url = root + "login"
    response = client.post(url, data=dict(token=access))
    assert response.status_code == 200

def test_bad_login(client, mocker):
    mocker.patch("core.api.auth.parse_oauth", return_value="badlogin@integrichain.com")
    url = root + "login"
    response = client.post(url, data=dict(token="foo"))
    assert response.status_code == 403

def test_no_login(client):
    url = root + "login"
    response = client.get(url)
    assert response.status_code == 405

def test_valid_cookie(client, mocker):
    mocker.patch("core.api.auth.parse_oauth", return_value="njb@integrichain.com")
    url = root + "login"
    url2 = root + "validate"
    client.post(url, data=dict(token=access))
    response = client.post(url2, data=dict(token=access))
    assert response.status_code == 200

def test_invalid_cookie(client, mocker):
    mocker.patch("core.api.auth.parse_oauth", return_value="badlogin@integrichain.com")
    url = root + "login"
    url2 = root + "validate"
    client.post(url, data=dict(token=access))
    response = client.post(url2, data=dict(token="foo"))
    assert response.status_code == 403

def test_no_cookie(client):
    url = root + "login"
    url2 = root + "validate"
    client.post(url, data=dict(token=access))
    response = client.get(url2)
    assert response.status_code == 405