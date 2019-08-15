import pytest
import paramiko
import mock
from unittest.mock import MagicMock, patch
from nightcrawler.crawler import Nightcrawler


class TestNightcrawler:

    @patch('nightcrawler.crawler.paramiko.Transport', autospec=True)
    @patch('nightcrawler.crawler.paramiko.SFTPClient')
    def test_connect(self, mock_sftp, mock_transport):


        mock_creds = {
            'host': 'host',
            'user': 'user',
            'password': 'password',
            'port': '22'
        }

        crawl = Nightcrawler(mock_creds)
        crawl.transport.connect.assert_called_with(username='user', password='password')
    
    # def test_file_crawl(self):
