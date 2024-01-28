from dataclasses import dataclass
from typing import Optional

import musicbrainzngs
from dateutil import parser
from rich import print
from rich.prompt import IntPrompt


@dataclass
class UserAgent:
    """
    We need to set the user agent when using musicbrainzngs,
    and this is a lil class to make sense of the different values.
    """
    agent: str
    version: str
    url: str


@dataclass
class Track:
    track_title: str
    disc_no: Optional[int]
    track_position: int
    track_length: int

    @classmethod
    def parse_musicbrainz_result(cls, result: dict, disc_no: Optional[int] = 1):
        """
        Look deep into the eyes of the json response and extract the track values we care about.
        """
        track_position: int = int(result['position'])
        title: str = result['recording']['title']
        length: int = int(result['length']) / 1000

        return Track(title, disc_no, track_position, length)

    def __str__(self):
        return f"🎵 {self.track_position} {self.track_title}"


@dataclass
class CD:
    id: str
    title: str
    artist: str
    year: Optional[str]
    discs: int
    tracks: Optional[list[Track]] = None

    def __post_init__(self):
        self._get_tracks()

    @classmethod
    def find_cd(cls, barcode: str, choice: bool = True):
        """
        The big method of this class. This does the work of taking a barcode,
        calling MusicBrainz to get release information, and offering the user
        a choice if the barcode pulls more than one CD release.
        """
        results = musicbrainzngs.search_releases(barcode=barcode)
        if not results['release-list']:
            raise RuntimeError(f"No releases found for {barcode}")
        else:
            releases = results['release-list']
            cds: list[CD] = [CD._parse_musicbrainz_result(release) for release in releases]

            if len(cds) < 2 or (not choice):
                return cds[0]
            else:
                print(f'More than one release matches barcode {barcode}.\n')
                index = 0
                for cd in cds:
                    index += 1
                    entry: str = (f"{index}. {cd.title}, {cd.discs} {'disc' if cd.discs < 2 else ' discs'}, "
                                  f"{len(cd.tracks)} tracks")
                    if cd.year:
                        entry += f", released in {cd.year}."
                    else:
                        entry += ", no release year found."
                    print(entry)
                print()

                release_choice = IntPrompt.ask("Which release do you want to scrobble?",
                                               choices=[str(x+1) for x in range(index)],
                                               default='1')
                return cds[int(release_choice)-1]

    @classmethod
    def _parse_musicbrainz_result(cls, result: dict):
        id: str = result['id']
        title: str = result['title']
        artist: str = result['artist-credit'][0]['name']
        year: str = str(parser.parse(result.get('date')).year) if 'date' in result and result['date'] else None
        disc_count: int = len(result['medium-list'])

        return CD(id, title, artist, year, disc_count)

    def _get_tracks(self) -> list[Track]:
        """
        Call MusicBrainz to get the track list for all CDs in the release.
        """
        result = musicbrainzngs.get_release_by_id(self.id, includes=['recordings'])
        self.tracks: list[Track] = []
        for disc in result['release']['medium-list']:
            self.tracks.extend([Track.parse_musicbrainz_result(track_result, disc['position'])
                                for track_result in disc['track-list']])

        return self.tracks

    def __str__(self):
        return f"💿 {self.artist} - {self.title} ({self.year})"

    def __len__(self):
        return len(self.tracks)


def init_musicbrainz(useragent: UserAgent):
    musicbrainzngs.set_useragent(useragent.agent, useragent.version, useragent.url)