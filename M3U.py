#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
M3U

BNF:
    M3U         ::= '#EXTM3U' ENTRY+
    ENTRY       ::= INFO FILENAME
    INFO        ::= '#EXTINF:' SECONDS ',' TITLE
    SECONDS     ::= -?\\d+
    TITLE       ::= .+
    FILENAME    ::= .+

Example:
    #EXTM3U

    #EXTINF:-1,You and I
    /home/mark/music/Queen/05-You_and_I.mp3
'''

import enum


class M3U:

    def __init__(self, filename=None):
        self.filename = filename
        self.dirty = False
        self._tracks = []
        if filename is not None:
            self.load()


    def load(self, filename=None):
        class Want(enum.Enum):
            M3U = enum.auto()
            INFO = enum.auto()
            FILENAME = enum.auto()

        if filename is not None:
            self.filename = filename
        self.clear()
        state = Want.M3U
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
                    track = Track(title.strip(), None, int(secs.strip()))
                    state = Want.FILENAME
                elif state is Want.FILENAME:
                    if line.startswith(EXTINF):
                        raise Error(
                            f'{lino}:unexpected {EXTINF} line: {line!r}')
                    track.filename = line
                    self._tracks.append(track)
                    state = Want.INFO
        self.dirty = False


    def save(self, filename=None):
        if filename is not None:
            self.filename = filename
        with open(self.filename, 'wt', encoding='utf-8') as file:
            file.write(f'{EXTM3U}\n\n')
            for track in self._tracks:
                file.write(f'{EXTINF}{track.secs},{track.title}\n'
                           f'{track.filename}\n\n')
        self.dirty = False


    def clear(self):
        self._tracks.clear()
        self.dirty = True


    def movedown(self, index):
        if index + 1 < len(self._tracks):
            x = self._tracks[index]
            y = self._tracks[index + 1]
            self._tracks[index] = y
            self._tracks[index + 1] = x
            self.dirty = True
            return True
        return False


    def moveup(self, index):
        if index > 0:
            x = self._tracks[index]
            y = self._tracks[index - 1]
            self._tracks[index] = y
            self._tracks[index - 1] = x
            self.dirty = True
            return True
        return False


    def __len__(self):
        return len(self._tracks)


    def __iadd__(self, track):
        self._tracks.append(track)
        self.dirty = True
        return self


    def __getitem__(self, index):
        return self._tracks[index]


    def __setitem__(self, index, track):
        self._tracks[index] = track
        self.dirty = True


    def __delitem__(self, index):
        self.dirty = True
        return self._tracks.pop(index)


    def __iter__(self):
        return iter(self._tracks)


class Track:

    def __init__(self, title, filename, secs=-1):
        self.title = title
        self.filename = filename
        self.secs = secs


    def __bool__(self):
        return self.title and self.filename


    def __eq__(self, other):
        return (self.title == other.title and self.secs == other.secs and
                self.filename == other.filename)


    def __repr__(self):
        return (f'{self.__class__.__name__}({self.title!r}, '
                f'{self.filename!r}, {self.secs!r})')


class Error(Exception):
    pass


EXTM3U = '#EXTM3U'
EXTINF = '#EXTINF:'
