#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import sys

import playlist


def main():
    # TODO replace with GUI

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = pathlib.Path.home() / 'data/playlists/Van Morrison.m3u'
    tracks = playlist.Playlist(filename)
    print(f'Playlist: {tracks.filename!r} of {len(tracks)} tracks:')
    assert not tracks.dirty
    for i, track in enumerate(tracks, 1):
        print(f'{i: >4d}: {track.title}\t{track.filename}')


if __name__ == '__main__':
    main()
