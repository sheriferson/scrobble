import pytest
from scrobble.utils import Config

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