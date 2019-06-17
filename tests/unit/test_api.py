import pytest
import json
from core.api import app
access = "doesn't matter, oauth validation is mock.patched"
root = "/config_api"
oauth = "core.api.routes.auth.parse_oauth"  # patch target


@pytest.fixture
def logged_client(mocker):
    mocker.patch(oauth, return_value="njb@integrichain.com")
    url = root + "/login"
    flask = app.create_app()
    client = flask.test_client()
    client.environ_base['HTTP_AUTHORIZATION'] = access
    client.get(url)
    yield client


@pytest.fixture
def client(mocker):
    flask = app.create_app()
    client = flask.test_client()
    yield client


def test_good_login(client, mocker):
    mocker.patch(oauth, return_value="njb@integrichain.com")
    client.environ_base['HTTP_AUTHORIZATION'] = access
    url = root + "/login"
    response = client.get(url)
    assert response.status_code == 200


def test_bad_login(client, mocker):
    mocker.patch(oauth, return_value="badlogin@integrichain.com")
    client.environ_base['HTTP_AUTHORIZATION'] = access
    url = root + "/login"
    response = client.get(url)
    assert response.status_code == 403


def test_no_login(client):
    url = root + "/login"
    response = client.get(url)
    assert response.status_code == 401


def test_valid_cookie(logged_client, mocker):
    url = root + "/validate"
    response = logged_client.get(url)
    assert response.status_code == 200


def test_invalid_cookie(logged_client, mocker):
    url = root + "/validate"
    logged_client.environ_base['HTTP_AUTHORIZATION'] = "foo"
    response = logged_client.get(url)
    assert response.status_code == 403


def test_no_cookie(logged_client):
    url = root + "/validate"
    logged_client.environ_base = None
    response = logged_client.get(url)
    assert response.status_code == 401


def test_index(logged_client):
    url = root + "/index"
    response = logged_client.get(url)
    try:
        json.loads(response.get_data())
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON response")
    assert response.status_code == 200


def test_unlogged_index(client):
    url = root + "/index"
    response = client.get(url)
    assert response.status_code == 401


def test_filters(logged_client):
    url = root + "/filters"
    response = logged_client.get(url)
    try:
        json.loads(response.get_data())
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON response")
    assert response.status_code == 200


def test_unlogged_filters(client):
    url = root + "/filters"
    response = client.get(url)
    assert response.status_code == 401
