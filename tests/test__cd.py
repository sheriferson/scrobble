import pytest

from scrobble.musicbrainz import CD, UserAgent, init_musicbrainz

import importlib.metadata

USERAGENT = UserAgent('scrobble (PyPI) (tests)',
                      importlib.metadata.version('scrobble'),  # scrobble version
                      'https://github.com/sheriferson'
                      )

init_musicbrainz(USERAGENT)
TEST_CD = CD.find_cd(7277017746006, choice=False)


def test_cd_artist():
    assert TEST_CD.artist == 'Lacuna Coil'


def test_cd_album():
    assert TEST_CD.title == 'Comalies'


def test_cd_track_length():
    assert len(TEST_CD) == 14


def test_cd_string_representation():
    assert str(TEST_CD) == "💿 Lacuna Coil - Comalies (2002)"


def test_failed_CD_retrieval():
    with pytest.raises(RuntimeError):
        CD.find_cd(12345)
