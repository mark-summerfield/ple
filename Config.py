#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import atexit
import collections
import enum
import pathlib
import re

import Player
from Const import HISTORY_SIZE, HistoryItem
from playlist import M3U, PLS, XSPF


class _Config:

    def __init__(self):
        self.base_font_size = None
        self.current_playlist = ''
        self.current_track = ''
        self.current_volume = (Player.player.volume if Player.player.valid
                               else 0.5)
        self.default_playlist_suffix = M3U
        self.geometry = None
        self.music_path = None
        self.playlists_path = None
        self.cursor_blink_rate = None
        self.history = collections.deque()
        self._filename = None
        self.load()


    @property
    def filename(self):
        return self._filename


    def save(self):
        with open(self._filename, 'wt', encoding='utf-8') as file:
            file.write(f'''\
{_Key.BASEFONTSIZE.value} = {self.base_font_size}
{_Key.CURRENTPLAYLIST.value} = {self.current_playlist}
{_Key.CURRENTTRACK.value} = {self.current_track}
{_Key.CURRENTVOLUME.value} = {self.current_volume}
{_Key.DEFAULTPLAYLISTSUFFIX.value} = {self.default_playlist_suffix}
{_Key.GEOMETRY.value} = {self.geometry}
{_Key.MUSICPATH.value} = {self.music_path}
{_Key.PLAYLISTSPATH.value} = {self.playlists_path}
{_Key.CURSORBLINKRATE.value} = {self.cursor_blink_rate}
''')
            for i, item in enumerate(self.history, 1):
                file.write(f'History{i} = {item.playlist} | {item.track}\n')
                if i == HISTORY_SIZE:
                    break


    def load(self):
        self._set_defaults()
        if self._filename.exists():
            self._load()


    def _set_defaults(self):
        self.base_font_size = 11
        path = pathlib.Path.home()
        config = path / '.ple.ini'
        if not config.exists() and (path / '.config/').exists():
            config = path / '.config/ple.ini'
        self._filename = config
        if self.geometry is None:
            self.geometry = '800x600' # default size (& center position)
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
        self.cursor_blink_rate = 0 # no blinking


    def _load(self):
        self.history.clear()
        history = []
        with open(self._filename, 'rt', encoding='utf-8') as file:
            for lino, line in enumerate(file, 1):
                if not line or line[0] in ';#\n':
                    continue # skip blank lines and comments
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key = _Key.from_name(key_value[0])
                    if key is None:
                        print(f'{self._filename} #{lino}: skipping invalid '
                              f'key: {key_value[0]}')
                        continue
                    value = key_value[1].strip()
                    if not value:
                        continue # use already set default
                    err = None
                    if key is _Key.BASEFONTSIZE:
                        if value.isdecimal():
                            self.base_font_size = int(value)
                        else:
                            err = 'invalid int for'
                    elif key is _Key.CURRENTPLAYLIST:
                        self.current_playlist = value
                    elif key is _Key.CURRENTTRACK:
                        self.current_track = value
                    elif key is _Key.CURRENTVOLUME:
                        if value.replace('.', '').isdecimal():
                            self.current_volume = float(value)
                        else:
                            err = 'invalid float for'
                    elif key is _Key.DEFAULTPLAYLISTSUFFIX:
                        value = value.upper()
                        if not value.startswith('.'):
                            value = '.' + value
                        if value in {M3U, PLS, XSPF}:
                            self.default_playlist_suffix = value
                        else:
                            err = 'unrecognized playlist suffix'
                    elif key is _Key.GEOMETRY:
                        if re.fullmatch(r'\d+x\d+(?:[-+]\d+[-+]\d+)?',
                                        value):
                            self.geometry = value
                        else:
                            err = 'ill-formed'
                    elif key is _Key.MUSICPATH:
                        if pathlib.Path(value).is_dir():
                            self.music_path = value
                        else:
                            err = 'invalid or non-existent path for'
                    elif key is _Key.PLAYLISTSPATH:
                        if pathlib.Path(value).is_dir():
                            self.playlists_path = value
                        else:
                            err = 'invalid or non-existent path for'
                    elif key is _Key.CURSORBLINKRATE:
                        if value.isdecimal():
                            self.cursor_blink_rate = int(value)
                        else:
                            err = 'invalid integer for'
                    elif key in {_Key.HISTORY1, _Key.HISTORY2,
                                 _Key.HISTORY3, _Key.HISTORY4,
                                 _Key.HISTORY5, _Key.HISTORY6,
                                 _Key.HISTORY7}:
                        index = int(key.name[-1])
                        playlist, track = value.split('|')
                        history.append((index, HistoryItem(playlist.strip(),
                                                           track.strip())))
                    if err:
                        print(f'{self._filename} #{lino}: skipping '
                              f'{err} {key.value} {value!r}')
            if history:
                self.history += [item for _, item in sorted(history)]


@enum.unique
class _Key(enum.Enum):
    BASEFONTSIZE = 'Base Font Size'
    CURRENTPLAYLIST = 'Current Playlist'
    CURRENTTRACK = 'Current Track'
    CURRENTVOLUME = 'Current Volume'
    DEFAULTPLAYLISTSUFFIX = 'Default Playlist Suffix'
    GEOMETRY = 'Geometry'
    MUSICPATH = 'Music Path'
    PLAYLISTSPATH = 'Playlists Path'
    CURSORBLINKRATE = 'Cursor Blink Rate'
    HISTORY1 = 'History1'
    HISTORY2 = 'History2'
    HISTORY3 = 'History3'
    HISTORY4 = 'History4'
    HISTORY5 = 'History5'
    HISTORY6 = 'History6'
    HISTORY7 = 'History7'

    @classmethod
    def from_name(Class, name):
        name = re.sub(r'[-_.\s]+', '', name).upper()
        for key, member in Class.__members__.items():
            if key == name:
                return member


config = _Config()
atexit.register(config.save)
