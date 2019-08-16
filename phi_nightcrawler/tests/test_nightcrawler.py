import pytest
import paramiko
import mock
from unittest.mock import MagicMock, patch
from phi_nightcrawler.nightcrawler import Nightcrawler

@patch('phi_nightcrawler.nightcrawler.paramiko.Transport', autospec=True)
@patch('phi_nightcrawler.nightcrawler.paramiko.SFTPClient')
def test_mock_nightcrawler(mock_sftp, mock_transport):


    mock_creds = {
        'host': 'host',
        'user': 'user',
        'password': 'password',
        'port': '22'
    }

    crawl = Nightcrawler(mock_creds)
    crawl.transport.connect.assert_called_with(username='user', password='password')

    # mock_connect.assert_called_with(username='user', password='password')