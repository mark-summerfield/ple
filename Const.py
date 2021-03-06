#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import collections
import tkinter as tk

APPNAME = 'PLE'
VERSION = '1.4.1'

PAUSE_ICON = 'media-playback-pause.png'
PLAY_ICON = 'media-playback-start.png'

INFO_FG = 'navy'
WARN_FG = 'darkmagenta'
ERROR_FG = 'red'

PAD = '1m'
PAD3 = '3m'
NSWE = tk.N + tk.S + tk.W + tk.E
WE = tk.W + tk.E

HISTORY_LEN = 9

Bookmark = collections.namedtuple('Bookmark', 'playlist track')
