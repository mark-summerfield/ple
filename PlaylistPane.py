#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.ttk as ttk


class PlaylistPane(ttk.Frame):

    def __init__(self, master, *, padding):
        super().__init__(master, padding=padding)
        self.treeview = ttk.Treeview(self, selectmode=tk.BROWSE)
        yscroller = ttk.Scrollbar(self, orient=tk.VERTICAL,
                                  command=self.treeview.yview)
        xscroller = ttk.Scrollbar(self, orient=tk.HORIZONTAL,
                                  command=self.treeview.xview)
        self.treeview.configure(yscroll=yscroller.set,
                                xscroll=xscroller.set)
        self.treeview.heading('#0', text='Playlist', anchor=tk.W)
        self.treeview.grid(row=0, column=0,
                           sticky=tk.W + tk.E + tk.N + tk.S)
        yscroller.grid(row=0, column=1, sticky=tk.N + tk.S)
        xscroller.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.image = tk.PhotoImage(
            file=pathlib.Path(__file__).parent / f'images/{TRACK_ICON}')


    def clear(self):
        self.treeview.delete(*self.treeview.get_children())


    def set_tracks(self, tracks):
        self.clear()
        if tracks:
            for i, track in enumerate(tracks, 1):
                self.treeview.insert('', tk.END, track.filename,
                                     text=track.title, image=self.image)
            self.treeview.focus(tracks[0].filename)
            self.treeview.selection_set(tracks[0].filename)


TRACK_ICON = 'gmusicbrowser.png'
