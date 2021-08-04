#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import re


class Config:

    music_path = None
    playlists_path = None
    filename = None

    def __init__(self):
        if Config.music_path is None or Config.playlists_path is None:
            self.load()


    def load(self):
        path = pathlib.Path.home()
        config = path / '.config/ple.ini'
        if not config.exists():
            config = path / '.ple.ini'
        if config.exists():
            Config.filename = config
            key_val_re = re.compile(r'(?P<key>\w+)\s*=\s*(?P<value>).*')
            with open(Config.filename, 'rt', encoding='utf-8') as file:
                for line in file:
                    match = key_val_re.fullmatch(line)
                    if match is not None:
                        key = key_val_re.group('key')
                        value = key_val_re.group('value').strip()
                        if key.upper() == MUSICPATH and value:
                            Config.music_path = value
                        elif key.upper() == PLAYLISTSPATH and value:
                            Config.playlists_path = value
        if Config.music_path is None:
            music = path / 'Music'
            if not music.exists():
                music = path / 'music'
                if not music.exists():
                    music = path
            Config.music_path = music
        if Config.playlists_path is None:
            playlists = path / 'data/playlists'
            if not playlists.exists():
                playlists = path / 'playlists'
                if not playlists.exists():
                    playlists = path
            Config.playlists_path = playlists


    def save(self, *, music_path, playlists_path):
        Config.music_path = music_path
        Config.playlists_path = playlists_path
        if Config.filename is None:
            path = pathlib.Path.home()
            config = path / '.ple.ini'
            if not config.exists():
                config = path / '.config/ple.ini' # preferred
            Config.filename = config # may or may not exist
        with open(Config.filename, 'wt', encoding='utf-8') as file:
            file.write(f'{MUSICPATH}={music_path}\n'
                       f'{PLAYLISTSPATH}={playlists_path}\n')


MUSICPATH = 'MUSICPATH'
PLAYLISTSPATH = 'PLAYLISTSPATH'
