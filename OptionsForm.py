#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.filedialog
import tkinter.simpledialog as tkdialog
import tkinter.ttk as ttk

import Config
import playlist
from Const import APPNAME, PAD, PAD3, WE


class Form(tkdialog.Dialog):

    def __init__(self, master):
        self.suffixes = [playlist.M3U, playlist.PLS, playlist.XSPF]
        super().__init__(master, f'Options — {APPNAME}')


    def body(self, master):
        self.make_body_widgets(master)
        self.make_body_layout(master)
        self.make_body_bindings(master)
        return self.fontsize_spinbox


    def make_body_widgets(self, master):
        path = pathlib.Path(__file__).parent
        self.folder_icon = tk.PhotoImage(file=path / 'images/folder.png')
        config = Config.config
        self.filename_name_label = ttk.Label(master, text='Filename')
        self.filename_label = ttk.Label(master, text=config.filename,
                                        foreground='navy')
        self.fontsize_label = ttk.Label(master, text='Font Size',
                                        underline=0)
        self.fontsize_spinbox = ttk.Spinbox(master, from_=8, to=24)
        self.fontsize_spinbox.set(config.base_font_size)
        self.suffix_label = ttk.Label(master, text='Playlist Suffix',
                                      underline=9)
        self.suffix_combobox = ttk.Combobox(master, values=self.suffixes)
        self.suffix_combobox.state(['readonly'])
        try:
            index = self.suffixes.index(config.default_playlist_suffix)
        except ValueError:
            index = 0
        if index > -1:
            self.suffix_combobox.current(index)
        self.music_path_button = ttk.Button(
            master, text='Music Path…', underline=0,
            command=self.on_music_path, image=self.folder_icon,
            compound=tk.LEFT)
        self.music_path_label = ttk.Label(master, text=config.music_path,
                                          relief=tk.SUNKEN)
        self.playlists_path_button = ttk.Button(
            master, text='Playlists Path…', underline=0,
            command=self.on_playlists_path, image=self.folder_icon,
            compound=tk.LEFT)
        self.playlists_path_label = ttk.Label(
            master, text=config.playlists_path, relief=tk.SUNKEN)
        self.cursor_blink_rate_label = ttk.Label(
            master, text='Cursor Blink Rate', underline=7)
        self.cursor_blink_rate_spinbox = ttk.Spinbox(master, from_=0,
                                                     to=1000)
        self.cursor_blink_rate_spinbox.set(config.cursor_blink_rate)
        self.label = ttk.Label(
            master, text=f'Changes will be applied the next time {APPNAME} '
            'is started.', foreground='darkgreen')


    def make_body_layout(self, master):
        common = dict(padx=PAD, pady=PAD)
        self.filename_name_label.grid(row=0, column=0, sticky=tk.W,
                                      **common)
        self.filename_label.grid(row=0, column=1, sticky=WE, **common)
        self.fontsize_label.grid(row=1, column=0, sticky=tk.W, **common)
        self.fontsize_spinbox.grid(row=1, column=1, sticky=WE, **common)
        self.suffix_label.grid(row=2, column=0, sticky=tk.W, **common)
        self.suffix_combobox.grid(row=2, column=1, sticky=WE, **common)
        self.music_path_button.grid(row=3, column=0, sticky=WE, **common)
        self.music_path_label.grid(row=3, column=1, sticky=WE, **common)
        self.playlists_path_button.grid(row=4, column=0, sticky=WE,
                                        **common)
        self.playlists_path_label.grid(row=4, column=1, sticky=WE, **common)
        self.cursor_blink_rate_label.grid(row=5, column=0, sticky=tk.W,
                                          **common)
        self.cursor_blink_rate_spinbox.grid(row=5, column=1, sticky=WE,
                                            **common)
        self.label.grid(row=6, column=0, columnspan=2, sticky=WE, **common)


    def make_body_bindings(self, master):
        self.bind('<Alt-b>',
                  lambda *_: self.cursor_blink_rate_spinbox.focus_set())
        self.bind('<Alt-f>', lambda *_: self.fontsize_spinbox.focus_set())
        self.bind('<Alt-m>', lambda *_: self.music_path_button.invoke())
        self.bind('<Alt-p>', lambda *_: self.playlists_path_button.invoke())
        self.bind('<Alt-s>', lambda *_: self.suffix_combobox.focus_set())


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
        config = Config.config
        try:
            config.base_font_size = int(self.fontsize_spinbox.get())
        except ValueError:
            pass # just leave it as-is
        index = self.suffix_combobox.current()
        if index > -1:
            config.default_playlist_suffix = self.suffixes[index]
        config.music_path = self.music_path_label.cget('text')
        config.playlists_path = self.playlists_path_label.cget('text')
        try:
            config.cursor_blink_rate = int(
                self.cursor_blink_rate_spinbox.get())
        except ValueError:
            pass # just leave it as-is
        return True


    def on_music_path(self, _event=None):
        config = Config.config
        path = tkinter.filedialog.askdirectory(
            parent=self, title=f'Music Path — {APPNAME}',
            initialdir=config.music_path, mustexist=True)
        if path:
            self.music_path_label.config(text=path)


    def on_playlists_path(self, _event=None):
        config = Config.config
        path = tkinter.filedialog.askdirectory(
            parent=self, title=f'Playlists Path — {APPNAME}',
            initialdir=config.playlists_path, mustexist=True)
        if path:
            self.playlists_path_label.config(text=path)
