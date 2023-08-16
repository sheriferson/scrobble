import os
import pylast
from scrobble.utils import Config

SESSION_KEY_FILE = os.path.join(os.path.expanduser('~'), '.config', '.lastfm_session_key')
DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'scrobble.toml')


def get_lastfm_client(
        refresh_session_token: bool = False,
        scrobble_config_file: str = DEFAULT_CONFIG_PATH,
        session_key_file: str = SESSION_KEY_FILE,
        ) -> pylast.LastFMNetwork:

    config = Config(config_path=scrobble_config_file)
    if config.has_lastfm_api():
        network = pylast.LastFMNetwork(config.lastfm_api_key, config.lastfm_api_secret)
    else:
        raise RuntimeError(f'Last.fm api config in {session_key_file} is missing. Check README.md for instructrions.')

    # see https://github.com/pylast/pylast
    if refresh_session_token or not os.path.exists(SESSION_KEY_FILE):
        key_generator = pylast.SessionKeyGenerator(network)
        url = key_generator.get_web_auth_url()

        print(f"Please authorize scrobble (PyPI) to access your account:\n {url}\n")
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
