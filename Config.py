#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import atexit
import pathlib


class _Config:

    def __init__(self):
        self.music_path = None
        self.playlists_path = None
        self.geometry = None
        self._filename = None
        self.load()


    @property
    def filename(self):
        return self._filename


    def save(self):
        with open(self._filename, 'wt', encoding='utf-8') as file:
            file.write(f'{_GEOMETRY}={self.geometry}\n'
                       f'{_MUSICPATH}={self.music_path}\n'
                       f'{_PLAYLISTSPATH}={self.playlists_path}\n')


    def load(self):
        self._set_defaults()
        if self._filename.exists():
            self._load()


    def _set_defaults(self):
        path = pathlib.Path.home()
        config = path / '.ple.ini'
        if not config.exists() and (path / '.config/').exists():
            config = path / '.config/ple.ini'
        self._filename = config
        if self.geometry is None:
            self.geometry = '800x600+0+0' # default size & position
        if self.music_path is None:
            music = path / 'Music'
            if not music.exists():
                music = path / 'music'
                if not music.exists():
                    music = path
            self.music_path = music
        if self.playlists_path is None:
            playlists = path / 'data/playlists'
            if not playlists.exists():
                playlists = path / 'playlists'
                if not playlists.exists():
                    playlists = path
            self.playlists_path = playlists


    def _load(self):
        with open(self._filename, 'rt', encoding='utf-8') as file:
            for line in file:
                if not line or line[0] in ';#\n':
                    continue # skip blank lines and comments
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip().upper()
                    value = key_value[1].strip()
                    if key == _GEOMETRY and value:
                        self.geometry = value
                    elif key == _MUSICPATH and value:
                        self.music_path = value
                    elif key == _PLAYLISTSPATH and value:
                        self.playlists_path = value


_MUSICPATH = 'MUSICPATH'
_PLAYLISTSPATH = 'PLAYLISTSPATH'
_GEOMETRY = 'GEOMETRY'

config = _Config()
atexit.register(config.save)
