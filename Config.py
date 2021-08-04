#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import re

KEEP_EXISTING = object()


class Config:

    _music_path = None
    _playlists_path = None
    _filename = None
    _geometry = None


    @staticmethod
    def geometry(geometry_=None):
        if geometry_ is not None:
            Config._geometry = geometry_
        if Config._geometry is None:
            Config.load()
        return Config._geometry


    @staticmethod
    def music_path(folder=None):
        if folder is not None and pathlib.Path(folder).exists():
            Config._music_path = folder
        if Config._music_path is None:
            Config.load()
        return Config._music_path


    @staticmethod
    def playlists_path(folder=None):
        if folder is not None and pathlib.Path(folder).exists():
            Config._playlists_path = folder
        if Config._playlists_path is None:
            Config.load()
        return Config._playlists_path


    @staticmethod
    def filename():
        if Config._filename is None:
            Config.load()
        return Config._filename


    @staticmethod
    def load():
        path = pathlib.Path.home()
        config = path / '.config/ple.ini'
        if not config.exists():
            config = path / '.ple.ini'
        if config.exists():
            Config._filename = config
            key_val_re = re.compile(r'(?P<key>\w+)\s*=\s*(?P<value>).*')
            with open(Config._filename, 'rt', encoding='utf-8') as file:
                for line in file:
                    match = key_val_re.fullmatch(line)
                    if match is not None:
                        key = key_val_re.group('key')
                        value = key_val_re.group('value').strip()
                        if key.upper() == GEOMETRY and value:
                            Config._geometry = value
                        elif key.upper() == MUSICPATH and value:
                            Config._music_path = value
                        elif key.upper() == PLAYLISTSPATH and value:
                            Config._playlists_path = value
        if Config._geometry is None:
            Config._geometry = '800x600+0+0' # default size & position
        if Config._music_path is None:
            music = path / 'Music'
            if not music.exists():
                music = path / 'music'
                if not music.exists():
                    music = path
            Config._music_path = music
        if Config._playlists_path is None:
            playlists = path / 'data/playlists'
            if not playlists.exists():
                playlists = path / 'playlists'
                if not playlists.exists():
                    playlists = path
            Config._playlists_path = playlists


    @staticmethod
    def save(*, geometry_=KEEP_EXISTING, music_path_=KEEP_EXISTING,
             playlists_path_=KEEP_EXISTING):
        if geometry_ is not KEEP_EXISTING:
            Config._geometry = geometry_
        if music_path_ is not KEEP_EXISTING:
            Config._music_path = music_path_
        if playlists_path_ is not KEEP_EXISTING:
            Config._playlists_path = playlists_path_
        if Config._filename is None:
            path = pathlib.Path.home()
            config = path / '.ple.ini'
            if not config.exists():
                config = path / '.config/ple.ini' # preferred
            Config._filename = config # may or may not exist
        with open(Config._filename, 'wt', encoding='utf-8') as file:
            file.write(f'{GEOMETRY}={Config.geometry()}\n'
                       f'{MUSICPATH}={Config.music_path()}\n'
                       f'{PLAYLISTSPATH}={Config.playlists_path()}\n')


MUSICPATH = 'MUSICPATH'
PLAYLISTSPATH = 'PLAYLISTSPATH'
GEOMETRY = 'GEOMETRY'
