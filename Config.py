#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import atexit
import enum
import pathlib
import re


class _Config:

    def __init__(self):
        self.base_font_size = None
        self.geometry = None
        self.music_path = None
        self.playlists_path = None
        self._filename = None
        self.load()


    @property
    def filename(self):
        return self._filename


    def save(self):
        with open(self._filename, 'wt', encoding='utf-8') as file:
            file.write(f'''\
{_Key.BASEFONTSIZE.value} = {self.base_font_size}
{_Key.GEOMETRY.value} = {self.geometry}
{_Key.MUSICPATH.value} = {self.music_path}
{_Key.PLAYLISTSPATH.value} = {self.playlists_path}
''')


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


    def _load(self):
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
                    if err:
                        print(f'{self._filename} #{lino}: skipping '
                              f'{err} {key.value} {value!r}')


@enum.unique
class _Key(enum.Enum):
    BASEFONTSIZE = 'Base Font Size'
    GEOMETRY = 'Geometry'
    MUSICPATH = 'Music Path'
    PLAYLISTSPATH = 'Playlists Path'


    @classmethod
    def from_name(Class, name):
        name = re.sub(r'[-_.\s]+', '', name).upper()
        for key, member in Class.__members__.items():
            if key == name:
                return member


config = _Config()
atexit.register(config.save)
