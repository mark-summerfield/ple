#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import collections
import enum
import os
import re
import xml.etree.ElementTree as etree


class Playlist:

    def __init__(self, filename=None):
        self.filename = str(filename)
        self._dirty = False
        self._tracks = []
        if filename is not None:
            self.load()


    @property
    def dirty(self):
        return self._dirty


    def clear(self):
        self._tracks.clear()
        self._dirty = True


    def movedown(self, index):
        if index + 1 < len(self._tracks):
            return self._move(index, index + 1)
        return False


    def moveup(self, index):
        if index > 0:
            return self._move(index, index - 1)
        return False


    def _move(self, a, b):
        x = self._tracks[a]
        y = self._tracks[b]
        self._tracks[a] = y
        self._tracks[b] = x
        self._dirty = True
        return True


    def save(self, filename=None):
        if filename is not None:
            self.filename = str(filename)
        suffix = os.path.splitext(self.filename)[1].upper()
        saver = {'.M3U': self._save_m3u,
                 '.PLS': self._save_pls,
                 '.XSPF': self._save_xspf}.get(suffix, None)
        if saver is not None:
            return saver()
        raise Error(
            f'can\'t save unrecognized playlist format: {self.filename}')


    def load(self, filename=None):
        if filename is not None:
            self.filename = str(filename)
        suffix = os.path.splitext(self.filename)[1].upper()
        loader = {'.M3U': self._load_m3u,
                  '.PLS': self._load_pls,
                  '.XSPF': self._load_xspf}.get(suffix, None)
        if loader is not None:
            return loader()
        raise Error(
            f'can\'t load unrecognized playlist format: {self.filename}')


    def _save_m3u(self):
        with open(self.filename, 'wt', encoding='utf-8') as file:
            file.write(f'{EXTM3U}\n\n')
            for track in self._tracks:
                file.write(f'{EXTINF}{track.secs},{track.title}\n'
                           f'{track.filename}\n\n')
        self._dirty = False


    def _load_m3u(self):
        '''
        BNF:
            M3U      ::= '#EXTM3U' ENTRY+
            ENTRY    ::= INFO FILENAME
            INFO     ::= '#EXTINF:' SECONDS ',' TITLE
            SECONDS  ::= -?\\d+
            TITLE    ::= .+
            FILENAME ::= .+

        Example:
            #EXTM3U

            #EXTINF:-1,You and I
            /home/mark/music/Queen/05-You_and_I.mp3
        '''
        class Want(enum.Enum):
            M3U = enum.auto()
            INFO = enum.auto()
            FILENAME = enum.auto()

        self.clear()
        state = Want.M3U
        title, secs, prev = None, None, None # title, secs: doc; prev: errs
        with open(self.filename, 'rt', encoding='utf-8') as file:
            for lino, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue # ignore blank lines
                if state is Want.M3U:
                    if line != EXTM3U:
                        raise Error(f'{lino}:invalid M3U header: {line!r}')
                    state = Want.INFO
                elif state is Want.INFO:
                    if not line.startswith(EXTINF):
                        raise Error(
                            f'{lino}:invalid {EXTINF} line: {line!r}')
                    secs, title = line[len(EXTINF):].split(',', 1)
                    prev = line
                    state = Want.FILENAME
                elif state is Want.FILENAME:
                    if line.startswith(EXTINF):
                        raise Error(
                            f'{lino}:unexpected {EXTINF} line: {line!r}')
                    title = title.strip()
                    secs = int(secs.strip()) or -1
                    if title and line:
                        self._tracks.append(Track(title, line, secs))
                    elif not title:
                        raise Error(f'{lino - 1}:missing title: {prev!r}')
                    elif not line:
                        raise Error(f'{lino}:missing filename: {line!r}')
                    title, secs = None, None
                    state = Want.INFO
        self._dirty = False


    def _save_pls(self):
        with open(self.filename, 'wt', encoding='utf-8') as file:
            file.write(f'{PLS_PLAYLIST}\n\n')
            for i, track in enumerate(self._tracks, start=1):
                file.write(f'{PLS_FILE}{i}={track.filename}\n'
                           f'{PLS_TITLE}{i}={track.title}\n'
                           f'{PLS_LENGTH}{i}={track.secs}\n\n')
            file.write(f'{PLS_NUMENTRIES}={len(self._tracks)}\n')
            file.write(f'{PLS_VERSION}=2\n')


    def _load_pls(self):
        '''
        BNF:
            PLS      ::= '[playlist]' ENTRY+ NUMBEROF? VERSION?
            ENTRY    ::= /File\\d+/ '=' FILENAME /Title\\d+/ '=' TITLE
                         /Length\\d+/ '=' \\d+
            FILENAME ::= .+
            TITLE    ::= .+
            NUMBEROF ::= 'NumberOfEntries' '=' \\d+
            VERSION  ::= 'Version' '=' \\d+

        Example:
            [playlist]

            File1=/home/mark/music/Amelie/01-J_y_suis_jamais_all.mp3
            Title1=J'y suis jamais allé
            Length1=-1

            NumberOfEntries=1
            Version=2

        '''
        item_rx = re.compile(r'^(?P<key>(?:File|Title|Length)(?P<n>\d+)|'
                             r'NumberOfEntries|Version)\s*=\s*'
                             r'(?P<value>.*)')
        self.clear()
        filenames = {}
        titles = {}
        lengths = {}
        with open(self.filename, 'rt', encoding='utf-8') as file:
            for lino, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue # ignore blank lines
                if line == PLS_PLAYLIST:
                    continue # ignore
                match = item_rx.match(line)
                if match is not None:
                    key = match.group('key')
                    if key in {PLS_NUMENTRIES, PLS_VERSION}:
                        continue # ignore these
                    else:
                        n = int(match.group('n'))
                        value = match.group('value')
                        if key.startswith(PLS_FILE):
                            filenames[n] = value
                        elif key.startswith(PLS_TITLE):
                            titles[n] = value
                        elif key.startswith(PLS_LENGTH):
                            lengths[n] = int(value) or -1
        for n, filename in sorted(filenames.items()):
            title = titles.get(n, None)
            secs = lengths.get(n, -1)
            if filename and title:
                self._tracks.append(Track(title, filename, secs))
        self._dirty = False


    def _load_xspf(self):
        self.clear()
        tree = etree.parse(self.filename)
        for track in tree.iter(f'{{{XSPF_NAMESPACE}}}{XSPF_TRACK}'):
            filename = track.find(f'{{{XSPF_NAMESPACE}}}{XSPF_LOCATION}')
            if filename is not None:
                filename = filename.text
                if filename.startswith('file://'):
                    filename = filename[7:]
            title = track.find(f'{{{XSPF_NAMESPACE}}}{XSPF_TITLE}')
            title = title.text if title is not None else None
            secs = track.find(f'{{{XSPF_NAMESPACE}}}{XSPF_DURATION}')
            secs = int(secs.text) // 1000 if secs is not None else -1
            if filename and title:
                self._tracks.append(Track(title, filename, secs))
        self._dirty = False


    def _save_xspf(self):
        builder = etree.TreeBuilder()
        builder.start(XSPF_PLAYLIST, dict(version='1',
                                          xmlns=XSPF_NAMESPACE))
        builder.start(XSPF_TRACKLIST)
        for track in self._tracks:
            builder.start(XSPF_TRACK)
            builder.start(XSPF_LOCATION)
            builder.data(f'file://{track.filename}')
            builder.end(XSPF_LOCATION)
            builder.start(XSPF_TITLE)
            builder.data(track.title)
            builder.end(XSPF_TITLE)
            if track.secs > 0:
                builder.start(XSPF_DURATION)
                builder.data(str(track.secs * 1000))
                builder.end(XSPF_DURATION)
            builder.end(XSPF_TRACK)
        builder.end(XSPF_TRACKLIST)
        builder.end(XSPF_PLAYLIST)
        tree = etree.ElementTree(builder.close())
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)


    def __len__(self):
        return len(self._tracks)


    def __iadd__(self, track):
        self._tracks.append(track)
        self._dirty = True
        return self


    def __getitem__(self, index):
        return self._tracks[index]


    def __setitem__(self, index, track):
        if self._tracks[index] != track:
            self._tracks[index] = track
            self._dirty = True


    def __delitem__(self, index):
        self._dirty = True
        return self._tracks.pop(index)


    def __iter__(self):
        return iter(self._tracks)


class Track(collections.namedtuple('Track', 'title filename secs')):

    __slots__ = ()

    def __bool__(self):
        return bool(self.title) and bool(self.filename)


    def __repr__(self):
        return (f'{self.__class__.__name__}({self.title!r}, '
                f'{self.filename!r}, {self.secs!r})')


class Error(Exception):
    pass


def create(folder, *, filename=None, suffix=None):
    '''creates a playlist for the given folder (and subfolders)

    If filename is specified the playlist's filename is set to it (so it
    must have a valid suffix, e.g.: .m3u .pls .xspf);
    Otherwise the filename is set to <folder>.m3u or to <folder><suffix> if
    suffix is not None.
    '''
    playlist = Playlist()
    playlist.filename = (str(filename) if filename is not None else
                         os.path.basename(str(folder)) + (suffix or '.m3u'))
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.upper().endswith(('.MP3', '.OGG', '.OGA')):
                fullname = os.path.join(root, filename)
                playlist += Track(normalize_name(filename), fullname, -1)
    playlist._tracks.sort(key=lambda track: track.filename.upper())
    return playlist


def normalize_name(name):
    normalize_rx = re.compile(
        r'^(?:[a-z]*\d+-)?(?P<name>.*)\.(?i:mp3|og[ga])$')
    i = name.rfind('/')
    if i == -1:
        i = name.rfind('\\')
    if i != -1:
        name = name[i + 1:]
    match = normalize_rx.match(name)
    if match is not None:
        name = match.group('name')
    else:
        i = name.rfind('.')
        if i > -1:
            name = name[:i]
    return name.replace('_', ' ')


EXTM3U = '#EXTM3U'
EXTINF = '#EXTINF:'
PLS_PLAYLIST = '[playlist]'
PLS_NUMENTRIES = 'NumberOfEntries'
PLS_VERSION = 'Version'
PLS_FILE = 'File'
PLS_TITLE = 'Title'
PLS_LENGTH = 'Length'
XSPF_NAMESPACE = 'http://xspf.org/ns/0/'
XSPF_PLAYLIST = 'playlist'
XSPF_TRACKLIST = 'trackList'
XSPF_TRACK = 'track'
XSPF_LOCATION = 'location'
XSPF_TITLE = 'title'
XSPF_DURATION = 'duration'
