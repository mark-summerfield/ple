#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
+----------------------------------------------------
|[New...][Open...] [Config...] [Save] [About]    [Quit]
+-----------------------------------------------------
| tree view showing    | list of titles (& times?) in
| folders +            | current (highlighted) playlist
| *.{m3u,pls,xspf}     | from left panel (if any)
|                      |
|         :            |             :
+-----------------------------------------------------
| [Add] [Rename] [Move Up] [Move Down] [Delete] [Prev] [Play|Pause] [Next] \
        [____position____] [___volume___]

New: create new empty playlist
Open: open folder
Config: default music folder; default playlists folder
Save: save the current playlist (Save As, if 'Unnamed')
About: show about box
Quit: offer save unsaved changes/quit/cancel if dirty then quit

Add: add one or more new tracks to the current playlist
Rename: rename the title of the current track in the current playlist
Move Up: move the current track up one in the current playlist
Move Down: move the current track down one in the current playlist
Delete: delete the current track from the current playlist
Prev: only show if default player is PLE
Play|Pause: if default player is external then only show [>] Play and
            when clicked send the current track to the player; if the track
            plays to the end automatically makes the next track current and
            starts playing it and so on until the end of the playlist
Next: only show if default player is PLE
position: progress slider MmSs/MmSs
volume: volume slider 0..100%
'''

import datetime
import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import Config
import Const
import PlaylistPane
import PlaylistsPane
import Tooltip


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=Const.PAD)
        self.images = {}
        self.make_images()
        self.make_widgets()
        self.make_layout()
        self.make_bindings()
        self.playlists_pane.set_focus()


    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (Const.FILEOPEN_ICON, Const.CONFIG_ICON,
                     Const.FILENEW_ICON,):
            self.images[name] = tk.PhotoImage(file=path / name)


    def make_widgets(self):
        self.make_buttons()
        self.playlists_pane = PlaylistsPane.PlaylistsPane(
            self.master, padding=Const.PAD,
            path=Config.config.playlists_path)
        self.a_playlist_pane = PlaylistPane.PlaylistPane(
            self.master, padding=Const.PAD)
        # TODO self.make_playlist_buttons()


    def make_buttons(self):
        self.button_frame = ttk.Frame(self.master)
        self.file_new_button = ttk.Button(
            self.button_frame, text='New…', underline=0, takefocus=False,
            image=self.images[Const.FILENEW_ICON],
            command=self.on_file_new, compound=tk.TOP)
        Tooltip.Tooltip(self.file_new_button, 'Create New Playlist… Ctrl+N')
        self.folder_open_button = ttk.Button(
            self.button_frame, text='Open…', underline=0, takefocus=False,
            image=self.images[Const.FILEOPEN_ICON],
            command=self.on_file_open, compound=tk.TOP)
        Tooltip.Tooltip(self.folder_open_button,
                        'Open Playlist Folder… Ctrl+O')
        self.config_button = ttk.Button(
            self.button_frame, text='Options…', takefocus=False,
            image=self.images[Const.CONFIG_ICON],
            command=self.on_config, compound=tk.TOP)
        Tooltip.Tooltip(self.config_button, f'Configure {Const.APPNAME}…')


    def make_layout(self):
        self.file_new_button.grid(row=0, column=0, padx=Const.PAD,
                                  sticky=tk.W)
        self.folder_open_button.grid(row=0, column=1, padx=Const.PAD,
                                     sticky=tk.W)
        self.config_button.grid(row=0, column=2, padx=Const.PAD,
                                sticky=tk.W)
        self.button_frame.grid(row=0, column=0, padx=Const.PAD,
                               pady=Const.PAD, sticky=tk.W + tk.E,
                               columnspan=2)
        self.playlists_pane.grid(row=1, column=0, padx=Const.PAD,
                                 pady=Const.PAD,
                                 sticky=tk.W + tk.E + tk.N + tk.S)
        self.a_playlist_pane.grid(row=1, column=1, padx=Const.PAD,
                                  pady=Const.PAD,
                                  sticky=tk.W + tk.E + tk.N + tk.S)
        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)


    def make_bindings(self):
        self.master.bind('<Alt-n>', self.on_file_new)
        self.master.bind('<Control-n>', self.on_file_new)
        self.master.bind('<Alt-o>', self.on_file_open)
        self.master.bind('<Control-o>', self.on_file_open)
        # self.master.bind('<Alt-s>', self.on_save)
        # self.master.bind('<Control-s>', self.on_save)
        self.master.bind('<Alt-q>', self.on_close)
        self.master.bind('<Control-q>', self.on_close)
        self.master.bind('<Escape>', self.on_close)


    def on_file_new(self, _event=None):
        print('on_file_new')


    def on_file_open(self, _event=None):
        print('on_file_open')


    def on_config(self, _event=None):
        print('on_config')


    def on_about(self, _event=None):
        year = datetime.date.today().year
        if year > 2020:
            year = f'2020-{year - 2000}'
        tk.messagebox.showinfo(f'{Const.APPNAME} — About', f'''\
{Const.APPNAME} v{Const.VERSION}

Copyright © {year} Mark Summerfield. All rights reserved.
License: GPLv3

An application for creating and modifying playlists and for playing \
tracks and playlists.''')


    def on_close(self, _event=None):
        # TODO prompt to save unsaved changes
        print('on_close(): prompt to save unsaved changes')
        self.quit()
