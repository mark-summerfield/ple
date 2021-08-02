#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import os
import sys

import playlist


def main():
    usage = USAGE.format(name=os.path.basename(sys.argv[0]))
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help', 'h', 'help'}:
        raise SystemExit(usage)
    tracks = playlist.Playist(sys.argv[1])
    updated = 0
    missing = 0
    total = 0
    for track in tracks:
        if track.secs <= 0:
            missing += 1
        else:
            total += track.secs
    if not missing:
        length = playlist.humanized_time(total)
        print(f'All tracks have non-zero times: {length}')


USAGE = '''usage: {name} <playlist>
reads the given playlist and for every missing time (e.g., -1 secs) tries to
replace the time with the actual play time, finishing by saving back the
updated playlist and outputing the playlist's total time.'''

if __name__ == '__main__':
    main()
