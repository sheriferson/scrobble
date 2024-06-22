from dataclasses import dataclass
from typing import Optional, Union

import musicbrainzngs
from dateutil import parser
from rich import print
from rich.prompt import IntPrompt

from scrobble.models.track import Track
from scrobble.models.cd import CD

DISC_NO_DECORATION = {
    '1': '₁',
    '2': '₂',
    '3': '₃',
    '4': '₄'
}


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
class MusicBrainzTrack(Track):

    @property
    def artist(self):
        if self.track_artist:
            return self.track_artist
        else:
            return ''
    @classmethod
    def parse_source_result(cls, result: dict, disc_no: Optional[int] = 1):
        """
        Look deep into the eyes of the json response and extract the track values we care about.
        """
        track_position: int = int(result['position'])
        title: str = result['recording']['title']
        track_artist: str = result['recording']['artist-credit'][0]['artist']['name']
        if 'length' in result:
            length: Union[int, float] = int(result['length']) / 1000
        elif 'track_or_recording_length' in result:
            length: Union[int, float] = int(result['track_or_recording_length']) / 1000
        else:
            raise RuntimeError(f"Couldn't find the length of track {result}")

        return MusicBrainzTrack(title, track_artist, disc_no, track_position, length)

    def __str__(self):
        if self.disc_no:
            return "💿{:>1} {:>2} {} - {}".format(DISC_NO_DECORATION[str(self.disc_no)], self.track_position, self.artist, self.track_title)
        else:
            return "🎵{:>2} {} - {}".format(self.track_position, self.artist, self.track_title)


@dataclass
class MusicBrainzCD(CD):
    id: str
    title: str
    artist: str
    year: Optional[str]
    discs: int
    _tracks: Optional[list[MusicBrainzTrack]] = None

    @property
    def tracks(self):
        if not self._tracks:
            self._tracks = self._get_tracks()
        return self._tracks

    @tracks.setter
    def tracks(self, new_tracks: Optional[list[MusicBrainzTrack]]):
        self._tracks = new_tracks

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
            cds: list[MusicBrainzCD] = [MusicBrainzCD._parse_musicbrainz_result(release) for release in releases]

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

        return MusicBrainzCD(id, title, artist, year, disc_count)

    def _get_tracks(self) -> list[MusicBrainzTrack]:
        """
        Call MusicBrainz to get the track list for all CDs in the release.
        """
        result = musicbrainzngs.get_release_by_id(self.id, includes=['recordings', 'artist-credits'])
        retrieved_tracks: list[MusicBrainzTrack] = []
        for disc in result['release']['medium-list']:
            retrieved_tracks.extend([MusicBrainzTrack.parse_source_result(track_result, disc['position'])
                                for track_result in disc['track-list']])

        return retrieved_tracks

    def __str__(self):
        return f"💿 {self.artist} - {self.title} ({self.year})"

    def __len__(self):
        return len(self.tracks)


def init_musicbrainz(useragent: UserAgent):
    musicbrainzngs.set_useragent(useragent.agent, useragent.version, useragent.url)