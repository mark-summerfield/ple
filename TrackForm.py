#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.simpledialog as tkdialog
import tkinter.ttk as ttk

import playlist
from Const import APPNAME, PAD


class Form(tkdialog.Dialog):

    def __init__(self, master, track):
        self.track = track
        self.edited_track = None
        self.title_var = tk.StringVar(value=self.track.title)
        super().__init__(master, f'Edit Track — {APPNAME}')


    def body(self, master):
        titleLabel = ttk.Label(master, text='Title:', underline=0)
        self.titleEntry = tk.Entry(
            master, textvariable=self.title_var, width=60)
        filenameLabel = ttk.Label(master, text='Filename:')
        filenameLabel2 = tk.Label(
            master, text=pathlib.Path(self.track.filename).name)
        common = dict(padx=PAD, pady=PAD)
        titleLabel.grid(row=0, column=0, sticky=tk.W)
        self.titleEntry.grid(row=0, column=1, sticky=tk.W + tk.E, **common)
        filenameLabel.grid(row=1, column=0, sticky=tk.W)
        filenameLabel2.grid(row=1, column=1, sticky=tk.W, **common)
        self.bind('<Alt-t>', lambda *_: self.titleEntry.focus_set())
        return self.titleEntry


    def buttonbox(self):
        path = pathlib.Path(__file__).parent
        self.ok_icon = tk.PhotoImage(file=path / 'images/dialog-ok.png')
        self.close_icon = tk.PhotoImage(
            file=path / 'images/dialog-close.png')
        box = ttk.Frame(self)
        okButton = ttk.Button(box, text='OK', underline=0, command=self.ok,
                              image=self.ok_icon, compound=tk.LEFT)
        closeButton = ttk.Button(
            box, text='Cancel', underline=0, command=self.cancel,
            image=self.close_icon, compound=tk.LEFT)
        okButton.pack(side=tk.LEFT, pady=PAD, padx=PAD * 3)
        closeButton.pack(side=tk.RIGHT, pady=PAD, padx=PAD * 3)
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
