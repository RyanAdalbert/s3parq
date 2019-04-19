import pytest
from core.api import app

# you can generate an access token at https://developers.google.com/oauthplayground/
# the access token only needs authorization for userinfo.email and userinfo.profile
access = "ya29.GlvwBi1w-hyHUHhqPSnJY96-1DKwjzJWlhrxnRzMZhDdba9Ec4FT_EAjDoLd6IY7ASu3M6k4Q6y4TJ6Bo2a0kMrXgzk4yKMu5dqLdh0ab4wkZzGL1i9avf-QfeYe"
root = "/config_api/"

@pytest.fixture
def client():
    flask = app.create_app()
    client = flask.test_client()
    yield client

def test_good_login(client):
    url = root + "login"
    response = client.post(url, data=dict(token=access))
    assert response.status_code == 200

def test_bad_login(client):
    url = root + "login"
    response = client.post(url, data=dict(token="foo"))
    assert response.status_code == 403

def test_no_login(client):
    url = root + "login"
    response = client.get(url)
    assert response.status_code == 400

def test_valid_cookie(client):
    url = root + "login"
    url2 = root + "validate"
    client.post(url, data=dict(token=access))
    response = client.post(url2, data=dict(token=access))
    assert response.status_code == 200

def test_invalid_cookie(client):
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
    assert response.status_code == 400