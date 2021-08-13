#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.simpledialog as tkdialog
import tkinter.ttk as ttk

import playlist
from Const import APPNAME, INFO_FG, PAD


class Form(tkdialog.Dialog):

    def __init__(self, master, track):
        self.track = track
        self.edited_track = None
        self.title_var = tk.StringVar(value=self.track.title)
        self.title_var.trace_add('write', self.update_ui)
        super().__init__(master, f'Edit Track — {APPNAME}')


    def body(self, master):
        title_label = ttk.Label(master, text='Title:', underline=0)
        self.title_entry = tk.Entry(
            master, textvariable=self.title_var, width=60)
        if self.track.secs > 0:
            duration_name_label = ttk.Label(master, text='Duration:')
            duration_label = ttk.Label(
                master, text=playlist.humanized_length(self.track.secs),
                foreground=INFO_FG)
        filename_name_label = ttk.Label(master, text='Filename:')
        filename_label = tk.Label(
            master, text=pathlib.Path(self.track.filename).name,
            foreground=INFO_FG)
        common = dict(padx=PAD, pady=PAD)
        title_label.grid(row=0, column=0, sticky=tk.W)
        self.title_entry.grid(row=0, column=1, sticky=tk.W + tk.E, **common)
        if self.track.secs > 0:
            duration_name_label.grid(row=1, column=0, sticky=tk.W)
            duration_label.grid(row=1, column=1, sticky=tk.W, **common)
        filename_name_label.grid(row=2, column=0, sticky=tk.W)
        filename_label.grid(row=2, column=1, sticky=tk.W, **common)
        self.bind('<Alt-t>', lambda *_: self.title_entry.focus_set())
        return self.title_entry


    def buttonbox(self):
        path = pathlib.Path(__file__).parent
        self.ok_icon = tk.PhotoImage(file=path / 'images/dialog-ok.png')
        self.close_icon = tk.PhotoImage(
            file=path / 'images/dialog-close.png')
        box = ttk.Frame(self)
        self.ok_button = ttk.Button(
            box, text='OK', underline=0, command=self.ok,
            image=self.ok_icon, compound=tk.LEFT)
        close_button = ttk.Button(
            box, text='Cancel', underline=0, command=self.cancel,
            image=self.close_icon, compound=tk.LEFT)
        self.ok_button.pack(side=tk.LEFT, pady=PAD, padx=PAD)
        ttk.Label(box, text=' ').pack(side=tk.LEFT) # Padding
        close_button.pack(side=tk.RIGHT, pady=PAD, padx=PAD)
        box.pack()
        self.bind('<Return>', self.ok)
        self.bind('<Alt-o>', self.ok)
        self.bind('<Escape>', self.cancel)
        self.bind('<Alt-c>', self.cancel)


    def validate(self):
        title = self.title_var.get()
        is_valid = bool(title)
        if is_valid:
            track = playlist.Track(title, self.track.filename,
                                   self.track.secs)
            if track != self.track:
                self.edited_track = track
        return is_valid


    def update_ui(self, *_):
        state = tk.DISABLED
        if self.title_var.get().strip():
            state = '!' + state
        self.ok_button.state([state])
