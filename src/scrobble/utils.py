import os
import tomllib
from dataclasses import dataclass
from datetime import datetime
import subprocess
from typing import Optional

from scrobble.musicbrainz import CD
from scrobble.musicbrainz import Track


def read_api_keys(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f'.toml config file not found in {config_path}')
    with open(config_path, 'rb') as config_file:
        keys = tomllib.load(config_file)

    return keys


@dataclass
class Config:
    config_path: str = os.path.join(os.path.expanduser('~'), '.config', 'scrobble.toml')
    lastfmapi: Optional[dict[str, str]] = None
    pushoverapi: Optional[dict[str, str]] = None

    def __post_init__(self):
        keys = read_api_keys(self.config_path)
        self.lastfmapi = keys['lastfmapi']

        if 'pushoverapi' in keys:
            self.pushoverapi = keys['pushoverapi']
        else:
            self.pushoverapi = None

    def has_lastfm_api(self):
        if self.lastfmapi and 'api_key' in self.lastfmapi and 'api_secret' in self.lastfmapi:
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

    @lastfm_username.setter
    def lastfm_username(self, new_lastfm_username):
        if new_lastfm_username:
            self.lastfmapi['username'] = new_lastfm_username
        else:
            raise ValueError('You cannot set the Last.fm username to an empty value.')

    @property
    def lastfm_api_key(self):
        return self.lastfmapi['api_key']

    @property
    def lastfm_api_secret(self):
        return self.lastfmapi['api_secret']

    @property
    def pushover_token(self):
        return self.pushoverapi['token']

    @pushover_token.setter
    def pushover_token(self, new_token_value: str):
        if new_token_value:
            self.pushoverapi['token'] = new_token_value
        else:
            raise ValueError('You cannot set the Pushover token to an empty value.')

    @property
    def pushover_user(self):
        return self.pushoverapi['user_key']

    @pushover_user.setter
    def pushover_user(self, new_pushover_user: str):
        if new_pushover_user:
            self.pushoverapi['user_key'] = new_pushover_user
        else:
            raise ValueError('You cannot set the Pushover user key to an empty value.')


def prepare_tracks(cd: CD, tracks: list[Track], playback_end: str = 'now') -> list[dict]:
    total_run_time: int = 0
    for track in tracks:
        total_run_time += track.track_length

    if playback_end != 'now':
        import parsedatetime
        cal = parsedatetime.Calendar()
        try:
            parsed_end, _ = cal.parse(playback_end)
            stop_time = datetime(*parsed_end[:6]).timestamp()
        except:
            raise ValueError(f"'{playback_end}' could not be parsed. Try a different input.")

    else:
        stop_time = datetime.now().timestamp()

    start_time = int(stop_time) - total_run_time
    elapsed: int = 0

    prepped_tracks = []
    for track in tracks:
        elapsed += track.track_length
        prepped_tracks.append(
            {
                'artist': cd.artist,
                'title': track.track_title,
                'album': cd.title,
                'timestamp': start_time + elapsed
            }
        )

    return prepped_tracks


def find_command(command: str):
    try:
        command_check = subprocess.check_output(
            f'which {command}',
            shell=True,
            encoding='UTF-8'
        ).rstrip()
    except subprocess.CalledProcessError:
        command_check = None

    return command_check


def choose_tracks(tracks: list[Track]) -> list[Track]:
    gum_path = find_command('gum')
    if gum_path:
        track_dict: dict = {str(track): track for track in tracks}
        choices = ' '.join(['"' + track_str + '"' for track_str in track_dict.keys()])
        pre_selections = ','.join(['"' + track_str + '"' for track_str in track_dict.keys()])
        picked_tracks = subprocess.check_output(
            f"{gum_path} choose {choices} --no-limit --selected={pre_selections}",
            env={'GUM_CHOOSE_HEIGHT': str(len(tracks))},
            shell=True,
            encoding='UTF-8').rstrip()

        return [track for track in tracks if str(track) in picked_tracks]

    else:
        raise NotImplementedError("Track choosing without charmbracelet/gum installation is not implemented yet.")
