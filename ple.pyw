#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
+----------------------------------------------------
|[Open...] [Config...] | [Add] [Edit] [Move Up] [Move Down] \
                         [Remove] [Save] [Quit]
                         [<<] [>#] [>!] [>>]
+-----------------------------------------------------
| tree view showing    | list of titles (& times?) in
| folders +            | current (highlighted) playlist
| *.{m3u,pls,xspf}     | from left panel (if any)
|                      |
|         :            |             :
+-----------------------------------------------------

Open: open folder
Config: default music folder; default playlists folder
        default player (PLE or external application)
Add: add one or more new tracks to the current playlist
Edit: edit the title of the current track in the current playlist
Move Up: move the current track up one in the current playlist
Move Down: move the current track down one in the current playlist
Remove: remove the current track from the current playlist
Save: save the current playlist
Quit: offer save unsaved changes/quit/cancel if dirty then quit
<< Play Prev: only show if default player is PLE
># Play|Pause: if default player is external then only show [>] Play and
               when clicked send the current track to the player
>! Play All: only visible if default player is external and when clicked
             send the current playlist to the player
>> Play Next: only show if default player is PLE
'''

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
