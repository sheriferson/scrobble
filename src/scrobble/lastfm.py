import os

import pylast

from scrobble.utils import Config

CONFIG = Config()


def get_lastfm_client(refresh_session_token: bool = False) -> pylast.LastFMNetwork:
    SESSION_KEY_FILE = os.path.join(os.path.expanduser('~'), '.config', '.lastfm_session_key')
    if CONFIG.has_lastfm_api:
        network = pylast.LastFMNetwork(CONFIG.lastfm_api_key, CONFIG.lastfm_api_secret)
    else:
        raise RuntimeError("Couldn't find Last.fm API key and secret to set up a client."
                           "Check README for instructions.")

    # see https://github.com/pylast/pylast
    if refresh_session_token or not os.path.exists(SESSION_KEY_FILE):
        key_generator = pylast.SessionKeyGenerator(network)
        url = key_generator.get_web_auth_url()

        print(f"Please authorize CD Scrobbler to access your account:\n {url}\n")
        import time
        import webbrowser

        webbrowser.open(url)

        while True:
            try:
                session_key = key_generator.get_web_auth_session_key(url)
                with open(SESSION_KEY_FILE, 'w') as session_key_file:
                    session_key_file.write(session_key)
                break
            except pylast.WSError:
                time.sleep(1)

    else:
        session_key = open(SESSION_KEY_FILE).read()

    network.session_key = session_key
    return network
