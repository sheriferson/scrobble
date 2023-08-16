import pytest
from scrobble.lastfm import get_lastfm_client

def test_bad_config_path():
    with pytest.raises(FileNotFoundError):
        lfmclient = get_lastfm_client(scrobble_config_file='/bad/file/path/here.toml')

def test_bad_config_missing_lastfm_key():
    with pytest.raises(RuntimeError):
        lfmclient = get_lastfm_client(scrobble_config_file='tests/resources/scrobble_bad_config.toml')
