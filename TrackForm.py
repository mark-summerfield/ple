#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.simpledialog as tkdialog
import tkinter.ttk as ttk

import playlist
from Const import APPNAME, INFO_FG, PAD, PAD3, WE


class Form(tkdialog.Dialog):

    def __init__(self, master, track):
        self.track = track
        self.edited_track = None
        self.title_var = tk.StringVar(value=self.track.title)
        self.title_var.trace_add('write', self.update_ui)
        super().__init__(master, f'Edit Track — {APPNAME}')


    def body(self, master):
        self.make_body_widgets(master)
        self.make_body_layout(master)
        self.make_body_bindings(master)
        return self.title_entry


    def make_body_widgets(self, master):
        self.title_label = ttk.Label(master, text='Title:', underline=0)
        self.title_entry = tk.Entry(master, textvariable=self.title_var,
                                    width=60)
        if self.track.secs > 0:
            self.duration_name_label = ttk.Label(master, text='Duration:')
            self.duration_label = ttk.Label(
                master, text=playlist.humanized_length(self.track.secs),
                foreground=INFO_FG)
        self.filename_name_label = ttk.Label(master, text='Filename:')
        self.filename_label = tk.Label(master, text=self.track.filename,
                                       foreground=INFO_FG)


    def make_body_layout(self, master):
        common = dict(padx=PAD, pady=PAD)
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        self.title_entry.grid(row=0, column=1, sticky=WE, **common)
        if self.track.secs > 0:
            self.duration_name_label.grid(row=1, column=0, sticky=tk.W)
            self.duration_label.grid(row=1, column=1, sticky=tk.W, **common)
        self.filename_name_label.grid(row=2, column=0, sticky=tk.W)
        self.filename_label.grid(row=2, column=1, sticky=tk.W, **common)


    def make_body_bindings(self, master):
        self.bind('<Alt-t>', lambda *_: self.title_entry.focus_set())


    def buttonbox(self):
        self.make_buttons()
        self.make_button_layout()
        self.make_button_bindings()


    def make_buttons(self):
        path = pathlib.Path(__file__).parent
        self.ok_icon = tk.PhotoImage(file=path / 'images/dialog-ok.png')
        self.close_icon = tk.PhotoImage(
            file=path / 'images/dialog-close.png')
        self.box = ttk.Frame(self)
        self.ok_button = ttk.Button(
            self.box, text='OK', underline=0, command=self.ok,
            image=self.ok_icon, compound=tk.LEFT)
        self.close_button = ttk.Button(
            self.box, text='Cancel', underline=0, command=self.cancel,
            image=self.close_icon, compound=tk.LEFT)


    def make_button_layout(self):
        self.ok_button.pack(side=tk.LEFT, padx=PAD)
        ttk.Frame(self.box, width=PAD).pack(side=tk.LEFT) # Padding
        self.close_button.pack(side=tk.RIGHT, padx=PAD)
        self.box.pack(pady=PAD3)


    def make_button_bindings(self):
        self.bind('<Return>', self.ok)
        self.bind('<Alt-o>', self.ok)
        self.bind('<Escape>', self.cancel)
        self.bind('<Alt-c>', self.cancel)


    def validate(self):
        self.edited_track = None
        title = self.title_var.get().strip()
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
