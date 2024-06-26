import pytest

from scrobble.musicbrainz import MusicBrainzCD, UserAgent, init_musicbrainz

import importlib.metadata

USERAGENT = UserAgent('scrobble (PyPI) (tests)',
                      importlib.metadata.version('scrobble'),  # scrobble version
                      'https://github.com/sheriferson'
                      )

init_musicbrainz(USERAGENT)
TEST_CD = MusicBrainzCD.find_cd(7277017746006, choice=False)


def test_cd_artist():
    assert TEST_CD.artist == 'Lacuna Coil'


def test_cd_album():
    assert TEST_CD.title == 'Comalies'


def test_cd_track_length():
    assert len(TEST_CD) == 14


def test_cd_track_length_alt_attribute_name():
    alt_test_cd: MusicBrainzCD = MusicBrainzCD.find_cd(4988005346872, choice=False)
    assert len(alt_test_cd) == 15
    assert alt_test_cd.tracks[0].track_length > 0

def test_cd_track_artist():
    assert TEST_CD.tracks[0].artist is not None

def test_cd_string_representation():
    assert str(TEST_CD) == "💿 Lacuna Coil - Comalies (2002)"


def test_failed_CD_retrieval():
    with pytest.raises(RuntimeError):
        MusicBrainzCD.find_cd(12345)
