#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import collections
import enum
import os
import re
import xml.etree.ElementTree as etree


M3U = '.M3U'
PLS = '.PLS'
XSPF = '.XSPF'


class Playlist:

    def __init__(self, filename):
        self.filename = str(filename)
        self._tracks = []
        if filename is not None and os.path.exists(filename):
            self.load()


    def clear(self):
        self._tracks.clear()


    @property
    def length(self):
        return sum(track.secs for track in self._tracks if track.secs > 0)


    @property
    def humanized_length(self, *, min_sign='′', sec_sign='″'):
        missing = False
        secs = 0
        for track in self._tracks:
            if track.secs <= 0:
                missing = True
            else:
                secs += track.secs
        if missing:
            if not secs:
                return 'unknown length'
            return 'at least ' + humanized_length(secs, min_sign=min_sign,
                                                  sec_sign=sec_sign)
        return humanized_length(secs, min_sign=min_sign, sec_sign=sec_sign)


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
        self.save()
        return True


    def save(self, filename=None):
        if filename is not None:
            self.filename = str(filename)
        suffix = os.path.splitext(self.filename)[1].upper()
        saver = {M3U: self._save_m3u,
                 PLS: self._save_pls,
                 XSPF: self._save_xspf}.get(suffix, None)
        if saver is not None:
            return saver()
        raise Error(
            f'can\'t save unrecognized playlist format: {self.filename}')


    def load(self, filename=None):
        if filename is not None:
            self.filename = str(filename)
        suffix = os.path.splitext(self.filename)[1].upper()
        loader = {M3U: self._load_m3u,
                  PLS: self._load_pls,
                  XSPF: self._load_xspf}.get(suffix, None)
        if loader is not None:
            return loader()
        raise Error(
            f'can\'t load unrecognized playlist format: {self.filename}')


    def _save_m3u(self):
        with open(self.filename, 'wt', encoding='utf-8') as file:
            file.write(f'{M3U_EXTM3U}\n\n')
            for track in self._tracks:
                file.write(f'{M3U_EXTINF}{track.secs},{track.title}\n'
                           f'{track.filename}\n\n')


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
                    if line != M3U_EXTM3U:
                        raise Error(f'{lino}:invalid M3U header: {line!r}')
                    state = Want.INFO
                elif state is Want.INFO:
                    if not line.startswith(M3U_EXTINF):
                        raise Error(
                            f'{lino}:invalid {M3U_EXTINF} line: {line!r}')
                    secs, title = line[len(M3U_EXTINF):].split(',', 1)
                    prev = line
                    state = Want.FILENAME
                elif state is Want.FILENAME:
                    if line.startswith(M3U_EXTINF):
                        raise Error(f'{lino}:unexpected {M3U_EXTINF} '
                                    f'line: {line!r}')
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


    def _load_xspf(self):
        self.clear()
        tree = etree.parse(self.filename)
        for track in tree.iter(f'{{{XSPF_NAMESPACE}}}{XSPF_TRACK}'):
            filename = track.find(f'{{{XSPF_NAMESPACE}}}{XSPF_LOCATION}')
            if filename is not None:
                filename = filename.text
                if filename.startswith(FILE_SCHEME):
                    filename = filename[7:]
            title = track.find(f'{{{XSPF_NAMESPACE}}}{XSPF_TITLE}')
            title = title.text if title is not None else None
            secs = track.find(f'{{{XSPF_NAMESPACE}}}{XSPF_DURATION}')
            secs = int(secs.text) // 1000 if secs is not None else -1
            if filename and title:
                self._tracks.append(Track(title, filename, secs))


    def _save_xspf(self):
        builder = etree.TreeBuilder()
        builder.start(XSPF_PLAYLIST, dict(version='1',
                                          xmlns=XSPF_NAMESPACE))
        builder.start(XSPF_TRACKLIST)
        for track in self._tracks:
            builder.start(XSPF_TRACK)
            builder.start(XSPF_LOCATION)
            builder.data(f'{FILE_SCHEME}{track.filename}')
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


    def insert(self, index, track):
        self._tracks.insert(index, track)
        self.save()


    def __len__(self):
        return len(self._tracks)


    def __iadd__(self, track):
        self._tracks.append(track)
        self.save()
        return self


    def __getitem__(self, index):
        return self._tracks[index]


    def __setitem__(self, index, track):
        if self._tracks[index] != track:
            self._tracks[index] = track
            self.save()


    def __delitem__(self, index):
        track = self._tracks.pop(index)
        self.save()
        return track


    def __iter__(self):
        return iter(self._tracks)


class Track(collections.namedtuple('Track', 'title filename secs')):

    __slots__ = ()

    def __bool__(self):
        return bool(self.title) and bool(self.filename)


    def __eq__(self, other):
        return (self.title == other.title and
                self.filename == other.filename and self.secs == other.secs)


    def __repr__(self):
        return (f'{self.__class__.__name__}({self.title!r}, '
                f'{self.filename!r}, {self.secs!r})')


class Error(Exception):
    pass


def is_playlist(filename):
    return filename.upper().endswith((M3U, PLS, XSPF))


def is_track(filename):
    return filename.upper().endswith(('.MP3', '.OGG', '.OGA'))


def filter(folder):
    '''yield all the supported music files in folder'''
    for root, _, files in os.walk(folder):
        for filename in files:
            if is_track(filename):
                yield os.path.join(root, filename)


def build(folder, *, format=M3U):
    '''build a playlist for the given folder (and subfolders)

    The filename is set to <folder>.m3u or to <folder>.<format> if
    format is not None.
    '''
    playlist_filename = os.path.basename(str(folder)) + format.lower()
    tracks = Playlist(playlist_filename)
    for filename in filter(folder):
        tracks += Track(normalize_name(filename), filename, -1)
    tracks._tracks.sort(key=lambda track: track.filename.upper())
    return tracks


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


def humanized_length(secs, *, min_sign='′', sec_sign='″'):
    if secs <= 0:
        return f'0{sec_sign}'
    hours, secs = divmod(secs, 3600)
    hrs = '{}h'.format(int(hours)) if hours else ''
    minutes, secs = divmod(secs, 60)
    mins = '{}{}'.format(int(minutes), min_sign) if minutes else ''
    if hours:
        return f'{hrs}{mins}'
    if minutes > 30:
        return f'{mins}'
    if minutes:
        return f'{mins}{int(secs)}{sec_sign}'
    return f'{max(1, secs)}{sec_sign}'


M3U_EXTM3U = '#EXTM3U'
M3U_EXTINF = '#EXTINF:'
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
FILE_SCHEME = 'file://'


if __name__ == '__main__':
    import sys

    def main():
        usage = USAGE.format(name=os.path.basename(sys.argv[0]))
        if len(sys.argv) == 1 or sys.argv[1] in {'h', 'help', '-h',
                                                 '--help'}:
            raise SystemExit(usage)
        what = sys.argv[1]
        args = sys.argv[2:]
        if not args:
            raise SystemExit(usage)
        if what in {'b', 'build'}:
            if len(args) > 2:
                raise SystemExit(usage)
            cli_build(args)
        elif what in {'c', 'convert'}:
            if len(args) < 2:
                raise SystemExit(usage)
            cli_convert(args)
        elif what in {'i', 'info'}:
            cli_info(args)
        else:
            raise SystemExit(usage)


    def cli_build(args):
        if len(args) == 2:
            format = args[0].lower()
            if not format.startswith('.'):
                format = '.' + format
            folder = args[1].rstrip('/\\')
        else:
            format = M3U.lower()
            folder = args[0].rstrip('/\\')
        tracks = build(folder, format=format)
        tracks.save()
        print(f'wrote {tracks.filename}')


    def cli_convert(args):
        format = args[0].lower()
        if not format.startswith('.'):
            format = '.' + format
        uformat = format.upper()
        for filename in args[1:]:
            if not is_playlist(filename):
                print(f'ignoring {filename}: unknown format')
            elif filename.upper().endswith(uformat):
                print(f'skipping {filename}: already in target format')
            else: # filename contains '.' because it ends with format
                tracks = Playlist(filename)
                tracks.save(filename[:filename.rfind('.')] + format)
                print(f'wrote {tracks.filename}')


    def cli_info(args):
        for filename in args:
            if is_playlist(filename):
                try:
                    tracks = Playlist(filename)
                    for track in tracks:
                        if not os.path.isfile(track.filename):
                            print(f'playlist {tracks.filename} has missing '
                                  f'track: {track.filename}')
                            break
                    else:
                        print(f'{len(tracks): 5,d} tracks taking '
                              f'{tracks.humanized_length}: '
                              f'{tracks.filename}')
                except Error:
                    pass
                except OSError as err:
                    print(err)

    USAGE = '''usage:
{name} <b|build> [format] <folder>
    Build a playlist based on the music files in folder and its subfolders
    and save it as dirname.format where dirname is the last component of
    folder's name and format is one of 'm3u', 'pls', 'xspf'.
{name} <c|convert> <format> <playlist1> [playlist2 [... [playlistN]]]
    Convert the or each playlist.ext to playlist.format where format is one
    of 'm3u', 'pls', 'xspf'.
{name} <i|info> <playlist1> [playlist2 [... [playlistN]]]
    Output the name and number of tracks in the given playlist(s) or report
    an error if one or more tracks doesn't actually exist.
{name} <h|help>
    Show this help message and quit.'''

    main()
