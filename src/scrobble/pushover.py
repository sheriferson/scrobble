import http.client
import urllib

from scrobble.musicbrainz import CD
from scrobble.utils import Config


def send_notification(cd: CD, config=None):
    if not config:
        config = Config()
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    query_strings = {
            "token": config.pushover_token,
            "user": config.pushover_user,
            "message": f"{cd.title} ({cd.year}) by {cd.artist} scrobbled to your account.",
        }

    if config.has_lastfm_username():
        query_strings["url"] = f"https://last.fm/user/{config.lastfm_username}"

    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(query_strings),
        {"Content-type": "application/x-www-form-urlencoded"}
    )
    return conn.getresponse()
