from typing import Optional

import typer
from typing_extensions import Annotated

from scrobble.lastfm import get_lastfm_client
from scrobble.musicbrainz import CD, UserAgent, init_musicbrainz
from scrobble.pushover import send_notification
from scrobble.utils import prepare_tracks

USERAGENT = UserAgent('CD Scrobbler',
                      '0.0.1',
                      'https://github.com/sheriferson'
                      )


APP = typer.Typer()


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
        choice: Annotated[bool, typer.Option(
            help='--choice will give you a list of options of more than one CD is matched. '
                 'Otherwise, the app will go with the first match.'
        )] = True,
        ):

    init_musicbrainz(USERAGENT)

    cd = CD.find_cd(barcode, choice)

    prepped_tracks = prepare_tracks(cd, playbackend)
    if verbose:
        print(cd)
        for track in cd.tracks:
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
