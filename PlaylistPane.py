#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import Treeview
from Const import NSWE, PAD


class PlaylistPane(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=PAD)
        self.treeview = Treeview.Treeview(self, selectmode=tk.BROWSE)
        self.treeview.heading('#0', text='Playlist', anchor=tk.CENTER)
        self.treeview.grid(row=0, column=0, sticky=NSWE)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.image = tk.PhotoImage(
            file=pathlib.Path(__file__).parent / f'images/{TRACK_ICON}')


    def clear(self):
        self.treeview.clear()


    def set_tracks(self, tracks):
        self.clear()
        if tracks:
            for track in tracks:
                self.treeview.insert('', tk.END, track.filename,
                                     text=track.title, image=self.image)
            self.treeview.focus(tracks[0].filename)
            self.treeview.selection_set(tracks[0].filename)


TRACK_ICON = 'gmusicbrowser.png'
