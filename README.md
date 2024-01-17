[![codecov](https://codecov.io/gh/sheriferson/scrobble/branch/main/graph/badge.svg?token=F5H7FXXB58)](https://codecov.io/gh/sheriferson/scrobble)

# Scrobble

A little very unofficial Python CLI tool to scrobble music to Last.fm.

> **Note**
> Super early, under active development, and so forth.


## Background

It started as a tool to scrobble CD tracklists using barcodes, and that's what it does today, but there are plans for it to do more.

Inspired by [CodeScrobble][] and [Open Scrobbler][].

[CodeScrobble]: https://codescrobble.com "CodeScrobble tool for scanning CD or record barcodes and scrobbling the tracklist."
[Open Scrobbler]: https://openscrobbler.com "Open Scrobbler tool for scrobbling albums or custom tracks."

## Features

- Scrobble a CD's tracklist using its barcode.
- Supports multi disc releases.
- Uses MusicBrainz as the source of CD and track metadata.
- Accepts an optional `PLAYBACKEND` argument in natural language if you want to scrobble a CD you listened to a while ago. e.g., `scrobble 016861828257 '2 hours ago'`.
- A `--dryrun` option if you just want to see a tracklist without sending anything to your last.fm account.
- A `--notify` option if you want to get a Pushover.net notification. Requires a Pushover app API token and a user key.
- If the barcode matches more than one release, the tool will ask you to choose. This matters because sometimes the tracklist is different (how releases that different end up with the same barcode is... pfff I don't know). If you want to yolo it, you can pass `--no-choice` and have the tool pick the first match.
- A `--track-choice` option that lets you choose a subset of tracks to scrobble. Requires [charmbracelet/gum][gum] for now.

[gum]: https://github.com/charmbracelet/gum "'gum' cli tool by charmbracelet. A tool for glamorous shell scripts."

## Installation

```sh
pip3 install scrobble
```

or

```sh
git clone https://github.com/sheriferson/scrobble
cd scrobble
pip3 install .
```

If you want to use the `--track-choice` option, you'll also need `gum`. See [here][gum] for details and Installation instructions. If you have Homebrew it's a simple:

```commandline
brew install gum
```

## Configuration

Okay you need to do some configuration before this will do anything useful for you. Some configurations are required (last.fm) and others are optional (Pushover).

You need to [get a last.fm API account][lastfmapi]. It's easy and immediate. Once you have a key and a secret, put them in `~/.config/scrobble.toml`:

[lastfmapi]: https://www.last.fm/api/account/create "Create a last.fm API account."

**Below is the mininum required configuration for this tool to work.**
```toml
[lastfmapi]
api_key = '<your-api-key>'
api_secret = '<your-api-secret>'
username = '<optional-username-for-url-in-pushover-notification>'
```

The first time you try to scrobble something, the app will ask you to give it permission to connect to your last.fm account, so you will need access to the machine's screen/browser. Once this is done, it will save a session key in `~/.lastfm_session_key`, and shouldn't need to ask for permission again.

If you want this tool to run on a remote/headless server, you can run the tool once on your local machine, then copy `~/.config/.lastfm_session_key` over your remote host.

If you plan on using `--notify` to get notifications when scrobbling is complete, you need to provide a Pushover API token and user key as well:


```toml
[pushoverapi]
token = '<your-pushover-app-token>'
user = '<your-user-key>'
```

## Usage

```sh
scrobble --help
```

```sh
  Usage: scrobble [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.              │
│ --show-completion             Show completion for the current shell, to copy it or   │
│                               customize the installation.                            │
│ --help                        Show this message and exit.                            │
╰──────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────╮
│ cd                                                                                   │
│ discogs                                                                              │
│ musicbrainz                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

```sh
scrobble cd --help
```

```sh
 Usage: scrobble cd [OPTIONS] BARCODE [PLAYBACKEND]

╭─ Arguments ──────────────────────────────────────────────────────────────────────────╮
│ *    barcode          TEXT           Barcode of the CD you want to scrobble. Double  │
│                                      album releases are supported.                   │
│                                      [default: None]                                 │
│                                      [required]                                      │
│      playbackend      [PLAYBACKEND]  When did you finish listening? e.g., 'now' or   │
│                                      '1 hour ago'.                                   │
│                                      [default: now]                                  │
╰──────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────╮
│ --dryrun            --no-dryrun              --dryrun will print a list of tracks    │
│                                              without scrobbling to Last.fm           │
│                                              [default: no-dryrun]                    │
│ --verbose           --no-verbose             --verbose will print a bunch of stuff   │
│                                              to your terminal.                       │
│                                              [default: no-verbose]                   │
│ --notify            --no-notify              --notify will send a push notification  │
│                                              via Pushover with CD information.       │
│                                              [default: no-notify]                    │
│ --release-choice    --no-release-choice      --release-choice will give you a list   │
│                                              of options of more than one CD is       │
│                                              matched. Otherwise, the app will go     │
│                                              with the first match.                   │
│                                              [default: release-choice]               │
│ --track-choice      --no-track-choice        --track-choice will give you a list of  │
│                                              tracks in the release to choose to      │
│                                              scrobble instead of scrobbling the      │
│                                              entire release.                         │
│                                              [default: no-track-choice]              │
│ --help                                       Show this message and exit.             │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

## Examples

```sh
# list album info and tracks from Rammstein's Herzeleid without actually scrobbling

$ scrobble cd --dryrun --verbose 031452916021

💿 Rammstein - Herzeleid (1996)
🎵 1 Wollt ihr das Bett in Flammen sehen?
🎵 2 Der Meister
🎵 3 Weißes Fleisch
🎵 4 Asche zu Asche
🎵 5 Seemann
🎵 6 Du riechst so gut
🎵 7 Das alte Leid
🎵 8 Heirate mich
🎵 9 Herzeleid
🎵 10 Laichzeit
🎵 11 Rammstein
⚠️  Dry run - no tracks were scrobbled.


# scrobble Nymphetamine by Cradle of Filth which you finished
# listening to two hours ago

$ scrobble cd 016861828257 '2 hours ago'

# scrobble Comalies by Lacuna Coil
# the barcode matches multiple releases, so you're offered options

$ scrobble cd 727701816029

More than one release matches barcode 727701816029.

1. Comalies, 1 disc, 13 tracks, released in 2002.
2. Comalies, 2  discs, 22 tracks, released in 2004.
3. Comalies, 1 disc, 13 tracks, released in 2002.

Which release do you want to scrobble? [1/2/3] (1):
...
# as you can see, sometimes there are duplicates
# differentiation between them isn't handled very well right now

# scrobble Fight Club: Original Motion Picture Score
# barcode matches multiple releases, but  don't ask me to choose a release,
# just pick the first one and send a notification using
# pushover.net (requires extra configuration)

$ scrobble cd --no-choice --notify 018777371520
```


## Missing

- Docs.
- Other features.
- More tests.
