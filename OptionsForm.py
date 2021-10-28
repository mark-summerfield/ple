#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.simpledialog as tkdialog
import tkinter.ttk as ttk

import Config
import playlist
from Const import APPNAME, PAD, PAD3, WE


class Form(tkdialog.Dialog):

    def __init__(self, master):
        super().__init__(master, f'Options — {APPNAME}')


    def body(self, master):
        self.make_body_widgets(master)
        self.make_body_layout(master)
        self.make_body_bindings(master)
        return self.fontsize_spinbox


    def make_body_widgets(self, master):
        config = Config.config
        self.filename_name_label = ttk.Label(master, text='Filename')
        self.filename_label = ttk.Label(master, text=config.filename,
                                        relief=tk.SUNKEN)
        self.fontsize_label = ttk.Label(master, text='Font Size',
                                        underline=0)
        self.fontsize_spinbox = ttk.Spinbox(master, from_=8, to=24)
        self.fontsize_spinbox.set(config.base_font_size)
        self.suffix_label = ttk.Label(master, text='Playlist Suffix',
                                      underline=10)
        values = [playlist.M3U, playlist.PLS, playlist.XSPF]
        self.suffix_combobox = ttk.Combobox(master, values=values)
        try:
            index = values.index(config.default_playlist_suffix)
        except ValueError:
            index = 0
        if index > -1:
            self.suffix_combobox.current(index)
        # TODO <Music Path> [              ] # button + sunken label
        # TODO <Playlists Path> [          ] # button + sunken label
        # TODO Cursor Blink Rate [         v] # label + spinbox


    def make_body_layout(self, master):
        common = dict(padx=PAD, pady=PAD)
        self.filename_name_label.grid(row=0, column=0, sticky=tk.W,
                                      **common)
        self.filename_label.grid(row=0, column=1, sticky=WE, **common)
        self.fontsize_label.grid(row=1, column=0, sticky=tk.W, **common)
        self.fontsize_spinbox.grid(row=1, column=1, sticky=WE, **common)
        self.suffix_label.grid(row=2, column=0, sticky=tk.W, **common)
        self.suffix_combobox.grid(row=2, column=1, sticky=WE, **common)
        # TODO <Music Path> [              ] # button + sunken label
        # TODO <Playlists Path> [          ] # button + sunken label
        # TODO Cursor Blink Rate [         v] # label + spinbox


    def make_body_bindings(self, master):
        self.bind('<Alt-f>', lambda *_: self.fontsize_spinbox.focus_set())
        self.bind('<Alt-s>', lambda *_: self.suffix_combobox.focus_set())
        # TODO <Music Path> [              ] # button + sunken label
        # TODO <Playlists Path> [          ] # button + sunken label
        # TODO Cursor Blink Rate [         v] # label + spinbox


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
        self.bind('<Return>', lambda *_: self.ok_button.invoke())
        self.bind('<Alt-o>', lambda *_: self.ok_button.invoke())
        self.bind('<Escape>', lambda *_: self.close_button.invoke())
        self.bind('<Alt-c>', lambda *_: self.close_button.invoke())


    def validate(self):
        # TODO if valid or if only valid entries possible, update config &
        # return True; else return False
        return True


    def update_ui(self, *_):
        pass # TODO delete if only valid entries possible?
        #state = tk.DISABLED
        #if self.title_var.get().strip():
        #    state = '!' + state
        #self.ok_button.state([state])
