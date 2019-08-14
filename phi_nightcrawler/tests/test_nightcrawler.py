import pytest
import paramiko
import mock
from unittest.mock import MagicMock, patch
from phi_nightcrawler.nightcrawler import Nightcrawler


class MockTransport:
    def __init__(self):
        return
    def connect(self, username, password):
        return True


@mock.patch('phi_nightcrawler.nightcrawler.Nightcrawler.paramiko.SFTPClient.from_transport')
@mock.patch('phi_nightcrawler.nightcrawler.Nightcrawler.paramiko.Transport.connect')
def test_mock_nightcrawler(mock_paramiko, mock_from_transport, monkeypatch):
    mock_creds = {
        'host': 'host',
        'user': 'user',
        'password': 'password',
        'port': '22'
    }

    mock_transport = MockTransport()
    mock_transport.connect = MagicMock()
    mock_paramiko.return_value = mock_transport
    monkeypatch.setattr(paramiko.Transport, 'connect', mock_transport)
    nc(mock_creds)
    mock_transport.connect.assert_called_with('user', 'password')

    # mock_connect.assert_called_with(username='user', password='password')