from typing import Optional

import typer
from typing_extensions import Annotated

from scrobble.lastfm import get_lastfm_client
from scrobble.musicbrainz import CD, UserAgent, init_musicbrainz
from scrobble.pushover import send_notification
from scrobble.utils import prepare_tracks, choose_tracks

import importlib.metadata


USERAGENT = UserAgent('scrobble (PyPI)',
                      importlib.metadata.version('scrobble'),
                      'https://github.com/sheriferson/scrobble'
                      )


APP = typer.Typer()

@APP.command()
def musicbrainz():
    raise NotImplementedError('Scrobbling a MusicBrainz release is not implemented yet.')

@APP.command()
def discogs():
    raise NotImplementedError('Scrobbling a Discogs release is not implemented yet.')

@APP.command()
def cd(
        barcode: Annotated[str, typer.Argument(
            help='Barcode of the CD you want to scrobble. Double album releases are supported.'
        )],
        playbackend: Annotated[Optional[str], typer.Argument(
            help="When did you finish listening? e.g., 'now' or '1 hour ago'."
        )] = 'now',

        dryrun: Annotated[bool, typer.Option(
            help='--dryrun will print a list of tracks without scrobbling to Last.fm'
        )] = False,
        verbose: Annotated[bool, typer.Option(
            help='--verbose will print a bunch of stuff to your terminal.'
        )] = False,
        notify: Annotated[bool, typer.Option(
            help='--notify will send a push notification via Pushover with CD information.'
        )] = False,
        release_choice: Annotated[bool, typer.Option(
            help='--release-choice will give you a list of options of more than one CD is matched. '
                 'Otherwise, the app will go with the first match.'
        )] = True,
        track_choice: Annotated[bool, typer.Option(
            help='--track-choice will give you a list of tracks in the release to choose to scrobble '
                 'instead of scrobbling the entire release.'
        )] = False,
        ):

    init_musicbrainz(USERAGENT)

    cd = CD.find_cd(barcode, release_choice)

    if track_choice:
        tracks_to_scrobble = choose_tracks(cd.tracks)
    else:
        tracks_to_scrobble = cd.tracks

    prepped_tracks = prepare_tracks(cd, tracks_to_scrobble, playbackend)

    if verbose:
        print(cd)
        for track in tracks_to_scrobble:
            print(track)

    if not dryrun:
        LASTFM = get_lastfm_client()
        LASTFM.scrobble_many(prepped_tracks)
    else:
        print('⚠️  Dry run - no tracks were scrobbled.')

    if notify:
        send_notification(cd)


def main():
    APP()
