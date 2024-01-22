from scrobble.pushover import send_notification
from scrobble.utils import Config
from scrobble.musicbrainz import CD, UserAgent, init_musicbrainz
import importlib.metadata
from urllib.parse import quote_plus

import unittest
from unittest.mock import patch, Mock

USERAGENT = UserAgent('scrobble (PyPI) (tests)',
                      importlib.metadata.version('scrobble'),  # scrobble version
                      'https://github.com/sheriferson'
                      )

init_musicbrainz(USERAGENT)

TEST_CD = CD.find_cd(7277017746006, choice=False)


class TestSendNotification(unittest.TestCase):

    @patch('http.client.HTTPSConnection')
    def test_send_notification(self, mock_https_connection):
        # Mocking the connection
        mock_conn_instance = Mock()
        mock_https_connection.return_value = mock_conn_instance

        # Mocking the response
        mock_response = Mock()
        mock_conn_instance.getresponse.return_value = mock_response

        # Example CD and Config objects
        config = Config(config_path='tests/resources/scrobble_complete_valid.toml')
        config.pushover_token = 'test_token'
        config.pushover_user = 'test_user'

        # Call the function with the mocked connection
        response = send_notification(TEST_CD, config)

        # Assert that conn.request was called with the expected arguments
        mock_conn_instance.request.assert_called_once_with(
            "POST",
            "/1/messages.json",
            f"token={config.pushover_token}&user={config.pushover_user}&message={quote_plus(TEST_CD.title)}+%28{TEST_CD.year}%29+by+{quote_plus(TEST_CD.artist)}+scrobbled+to+your+account.&url=https%3A%2F%2Flast.fm%2Fuser%2F{config.lastfm_username}",
            {"Content-type": "application/x-www-form-urlencoded"}
        )

        # Assert that conn.getresponse was called
        mock_conn_instance.getresponse.assert_called_once()

        # Assert that the function returned the expected response
        self.assertEqual(response, mock_response)
