from scrobble.musicbrainz import CD, UserAgent, init_musicbrainz

import importlib.metadata

USERAGENT = UserAgent('scrobble (PyPI) (tests)',
                      importlib.metadata.version('scrobble'),  # scrobble version
                      'https://github.com/sheriferson'
                      )

init_musicbrainz(USERAGENT)
test_cd = CD.find_cd(7277017746006, choice=False)


def test_cd_artist():
    assert test_cd.artist == 'Lacuna Coil'

def test_cd_album():
    assert test_cd.title == 'Comalies'

def test_cd_track_length():
    assert len(test_cd) == 14