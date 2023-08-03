import os
import tomllib
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from scrobble.musicbrainz import CD


@dataclass
class Config:
    config_path: str = os.path.join(os.path.expanduser('~'), '.config', 'scrobble.toml')
    lastfmapi: Optional[dict[str, str]] = None
    pushoverapi: Optional[dict[str, str]] = None

    def __post_init__(self):
        try:
            keys = self.read_api_keys(self.config_path)
            self.lastfmapi = keys['lastfmapi']
        except:
            raise RuntimeError(f"scrobble.toml not found in {self.config_path}")

        if 'pushoverapi' in keys:
            self.pushoverapi = keys['pushoverapi']
        else:
            self.pushoverapi = None

    def has_lastfm_api(self):
        if self.lastfmapi and self.lastfmapi['api_key'] and self.lastfmapi['api_secret']:
            return True
        else:
            return False

    def has_lastfm_username(self):
        if self.lastfmapi and ('username' in self.lastfmapi):
            return True
        else:
            return False

    @property
    def lastfm_username(self):
        return self.lastfmapi['username']

    @property
    def lastfm_api_key(self):
        return self.lastfmapi['api_key']

    @property
    def lastfm_api_secret(self):
        return self.lastfmapi['api_secret']

    @property
    def pushover_token(self):
        return self.pushoverapi['token']

    @property
    def pushover_user(self):
        return self.pushoverapi['user_key']

    def read_api_keys(self, config_path: str) -> dict:
        with open(config_path, 'rb') as config_file:
            keys = tomllib.load(config_file)

        return keys


def prepare_tracks(cd: CD, playbackend: str = 'now') -> list[dict]:
    total_run_time: int = 0
    for track in cd.tracks:
        total_run_time += track.track_length

    if playbackend != 'now':
        import parsedatetime
        cal = parsedatetime.Calendar()
        try:
            parsed_end, _ = cal.parse(playbackend)
            stop_time = datetime(*parsed_end[:6]).timestamp()
        except:
            raise ValueError(f"'{playbackend}' could not be parsed. Try a different input.")

    else:
        stop_time = datetime.now().timestamp()

    start_time = int(stop_time) - total_run_time
    elapsed: int = 0

    prepped_tracks = []
    for track in cd.tracks:
        elapsed += track.track_length
        prepped_tracks.append(
            {
                'artist': cd.artist,
                'title': track.track_title,
                'album': cd.title,
                'timestamp': start_time+elapsed
            }
        )

    return prepped_tracks
