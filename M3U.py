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


class M3U:

    def __init__(self, filename=None):
        self.filename = filename
        self.dirty = False
        self.tracks = []
        if filename is not None:
            self.load()


    def load(self, filename=None):
        if filename is not None:
            self.filename = filename
        self.clear()
        print('load', self.filename)
        self.dirty = False


    def save(self, filename=None):
        if filename is not None:
            self.filename = filename
        print('save', self.filename)
        self.dirty = False


    def clear(self):
        self.tracks.clear()
        self.dirty = True


    def movedown(self, index):
        if index + 1 < len(self.tracks):
            x = self.tracks[index]
            y = self.tracks[index + 1]
            self.tracks[index] = y
            self.tracks[index + 1] = x
            return True
        return False


    def moveup(self, index):
        if index > 0:
            x = self.tracks[index]
            y = self.tracks[index - 1]
            self.tracks[index] = y
            self.tracks[index - 1] = x
            return True
        return False


    def __len__(self):
        return len(self.tracks)


    def __iadd__(self, track):
        self.tracks.append(track)


    def __setitem__(self, index, track):
        self.tracks[index] = track


    def __delitem__(self, index):
        return self.tracks.pop(index)


    def __iter__(self):
        for track in self.tracks:
            yield track


class Track:

    def __init__(self, title, path, secs=-1):
        self.title = title
        self.path = path
        self.secs = secs

    # TODO __str__


if __name__ == '__main__':
    print('TESTS') # TODO
    # load, save, clear, movedown, moveup, len, +=, playlist[5] = track,
    # del playlist[5], for track in playlist: ...
