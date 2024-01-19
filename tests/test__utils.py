import unittest
from unittest.mock import patch

from scrobble.utils import Config, find_command, choose_tracks
from scrobble.musicbrainz import Track
from typing import List


TEST_TRACKS: List[Track] = [
            Track(track_title="track1", disc_no=1, track_position=1, track_length=10),
            Track(track_title="track1", disc_no=1, track_position=2, track_length=20),
            Track(track_title="track1", disc_no=1, track_position=3, track_length=30),
        ]

def test_valid_config_has_lastfm_api():
    test_config = Config(config_path='tests/resources/scrobble_complete_valid.toml')
    assert test_config.has_lastfm_api() == True

def test_valid_config_has_lastfm_username():
    test_config = Config(config_path='tests/resources/scrobble_complete_valid.toml')
    assert test_config.has_lastfm_username() == True

def test_valid_config_lastfm_api_key():
    test_config = Config(config_path='tests/resources/scrobble_complete_valid.toml')
    assert test_config.lastfm_api_key == 'fakelastfmapikey'

def test_valid_config_lastfm_username():
    test_config = Config(config_path='tests/resources/scrobble_complete_valid.toml')
    assert test_config.lastfm_username == 'thespeckofme'

def test_valid_config_pushover_token():
    test_config = Config(config_path='tests/resources/scrobble_complete_valid.toml')
    assert test_config.pushover_token == 'fakepushovertoken'

def test_find_command_succeeding():
    command_check = find_command('ls')
    assert command_check is not None

def test_find_command_returning_none():
    bad_command_check = find_command('badfakecommand')
    assert bad_command_check is None


class TestChooseTracksFunction(unittest.TestCase):
    @patch('scrobble.utils.find_command')
    @patch('subprocess.check_output')
    def test_choose_tracks_with_gum(self, mock_check_output, mock_find_command):
        mock_find_command.side_effect = lambda *args, **kwargs: '/path/to/gum'
        mock_check_output.return_value = f"{str(TEST_TRACKS[0])},{str(TEST_TRACKS[1])}"

        # Call the function
        result = choose_tracks(TEST_TRACKS)

        # Assert that the subprocess.check_output was called with the correct arguments
        mock_check_output.assert_called_once_with(
            f'/path/to/gum choose "{str(TEST_TRACKS[0])}" "{str(TEST_TRACKS[1])}" "{str(TEST_TRACKS[2])}"'
            f' --no-limit --selected="{str(TEST_TRACKS[0])}","{str(TEST_TRACKS[1])}","{str(TEST_TRACKS[2])}"',
            env={'GUM_CHOOSE_HEIGHT': '3'},
            shell=True,
            encoding='UTF-8'
        )

        # Assert that the result is as expected
        self.assertEqual(result, [TEST_TRACKS[0], TEST_TRACKS[1]])

    @patch('scrobble.utils.find_command')
    def test_choose_tracks_without_gum(self, mock_find_command):
        mock_find_command.return_value = None

        # Call the function and expect NotImplementedError to be raised
        with self.assertRaises(NotImplementedError):
            choose_tracks(TEST_TRACKS)