#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
+--------------------------------------------------------------------+
| [New]    +------------------------------------------+ [Add]        |
| [Open]   | tree view showing    | list of titles in | [Edit]       |
| [Config] | folders +            | current  playlist | [Move Up]    |
| [Save]   | *.{m3u,pls,xspf}     | from left panel   | [Move Down]  |
| [About]  |                      |                   | [Delete]     |
|          |         :            |             :     | [Prev]       |
|          |                      |                   | [Play|Pause] |
|          |                                          | [Next]       |
| Volume   |                                          | Position     |
| [  0%^v] +------------------------------------------+ [****......] |
+--------------------------------------------------------------------+

New: create new empty playlist
Open: open folder
Config: default music folder; default playlists folder
Save: save the current playlist (Save As, if 'Unnamed')
About: show about box
Quit: offer save unsaved changes/quit/cancel if dirty then quit
      (no explicit button: use Esc or Ctrl+Q or close button)

Add: add one or more new tracks to the current playlist
Edit: rename the title of the current track in the current playlist
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
import Player
import playlist
import PlaylistPane
import PlaylistsPane
import Tooltip


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=PAD)
        self.images = {}
        self.make_images()
        self.make_widgets()
        self.make_layout()
        self.make_bindings()
        self.playlists_pane.set_focus()
        if 1: # TODO delete (debugging)
            import random
            t = random.randint(60, 800)
            a = random.randint(0, t)
            self.set_progress(a, t)


    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (ADD_ICON, CONFIG_ICON, FILENEW_ICON, FILEOPEN_ICON):
            self.images[name] = tk.PhotoImage(file=path / name)


    def make_widgets(self):
        self.make_buttons()
        self.playlists_pane = PlaylistsPane.PlaylistsPane(
            self.master, padding=PAD, path=Config.config.playlists_path)
        self.a_playlist_pane = PlaylistPane.PlaylistPane(self.master,
                                                         padding=PAD)
        self.make_playlist_buttons()
        if Player.player.valid:
            self.make_scales()


    def make_buttons(self):
        self.button_frame = ttk.Frame(self.master)
        self.file_new_button = ttk.Button(
            self.button_frame, text='New…', underline=0, takefocus=False,
            image=self.images[FILENEW_ICON],
            command=self.on_file_new, compound=tk.TOP)
        Tooltip.Tooltip(self.file_new_button, 'Create New Playlist… Ctrl+N')
        self.folder_open_button = ttk.Button(
            self.button_frame, text='Open…', underline=0, takefocus=False,
            image=self.images[FILEOPEN_ICON],
            command=self.on_file_open, compound=tk.TOP)
        Tooltip.Tooltip(self.folder_open_button,
                        'Open Playlist Folder… Ctrl+O')
        self.config_button = ttk.Button(
            self.button_frame, text='Options…', takefocus=False,
            image=self.images[CONFIG_ICON],
            command=self.on_config, compound=tk.TOP)
        Tooltip.Tooltip(self.config_button, f'Configure {Const.APPNAME}…')


    def make_playlist_buttons(self):
        self.playlist_button_frame = ttk.Frame(self.master)
        self.add_button = ttk.Button(
            self.playlist_button_frame, text='Add…', underline=0,
            takefocus=False, image=self.images[ADD_ICON],
            command=self.on_add_track, compound=tk.TOP)
        Tooltip.Tooltip(self.add_button, 'Add Track to Playlist… Ctrl+A')


    def make_scales(self):
        self.volume_frame = ttk.Frame(self.master)
        self.volume_label = ttk.Label(self.volume_frame, text='Volume',
                                      underline=0)
        self.volume_spinbox = ttk.Spinbox(
            self.volume_frame, from_=0, to=100, wrap=False,
            format='%3.0f%%', width=5, justify=tk.RIGHT)
        self.volume_spinbox.set('50%')
        self.position_frame = ttk.Frame(self.master)
        self.position_label = ttk.Label(self.position_frame, text='0″/0″')
        self.position_progress = ttk.Label(
            self.position_frame, relief=tk.SUNKEN, width=PROGRESS_WIDTH,
            foreground='#8080FF', background='#FFFFCD',
            font=tk.font.nametofont('TkFixedFont'))


    def make_layout(self):
        self.make_button_layout()
        self.playlists_pane.grid(row=0, column=1, padx=PAD, pady=PAD,
                                 sticky=tk.W + tk.E + tk.N + tk.S)
        self.a_playlist_pane.grid(row=0, column=2, padx=PAD, pady=PAD,
                                  sticky=tk.W + tk.E + tk.N + tk.S)
        self.make_playlist_button_layout()
        if Player.player.valid:
            self.make_scales_layout()
        top = self.winfo_toplevel()
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        top.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)


    def make_button_layout(self):
        self.file_new_button.grid(row=0, column=0, pady=PAD, sticky=tk.N)
        self.folder_open_button.grid(row=1, column=0, pady=PAD, sticky=tk.N)
        self.config_button.grid(row=2, column=0, pady=PAD, sticky=tk.N)
        self.button_frame.grid(row=0, column=0, padx=PAD, pady=PAD,
                               sticky=tk.N + tk.S)


    def make_playlist_button_layout(self):
        self.add_button.grid(row=0, column=0, pady=PAD, sticky=tk.N)
        self.playlist_button_frame.grid(row=0, column=3, padx=PAD, pady=PAD,
                                        sticky=tk.N + tk.S)


    def make_scales_layout(self):
        self.volume_label.grid(row=0, column=0, padx=PAD, pady=PAD,
                               sticky=tk.S)
        self.volume_spinbox.grid(row=1, column=0, padx=PAD, pady=PAD,
                                 sticky=tk.S)
        self.volume_frame.grid(row=0, column=0, padx=PAD, pady=PAD,
                               sticky=tk.S)
        self.position_label.grid(row=0, column=0, padx=PAD, pady=PAD,
                                 sticky=tk.S)
        self.position_progress.grid(row=1, column=0, padx=PAD, pady=PAD,
                                    sticky=tk.S)
        self.position_frame.grid(row=0, column=3, padx=PAD, pady=PAD,
                                 sticky=tk.S)


    def make_bindings(self):
        self.master.bind('<Escape>', self.on_close)
        self.master.bind('<Alt-a>', self.on_add_track)
        self.master.bind('<Control-a>', self.on_add_track)
        self.master.bind('<Alt-n>', self.on_file_new)
        self.master.bind('<Control-n>', self.on_file_new)
        self.master.bind('<Alt-o>', self.on_file_open)
        self.master.bind('<Control-o>', self.on_file_open)
        self.master.bind('<Control-q>', self.on_close)
        # self.master.bind('<Alt-s>', self.on_save)
        # self.master.bind('<Control-s>', self.on_save)
        self.master.bind('<Alt-v>',
                         lambda *_: self.volume_spinbox.focus_set())


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
        Config.config.geometry = self.winfo_toplevel().geometry()
        self.quit()


    def on_add_track(self, _event=None):
        print('on_add_track')


    def set_progress(self, secs, total_secs):
        size = round((secs / total_secs) * PROGRESS_WIDTH)
        text = ('▉' * size) + ('▕' * (PROGRESS_WIDTH - size))
        self.position_progress.configure(text=text)
        secs = playlist.humanized_length(secs)
        total_secs = playlist.humanized_length(total_secs)
        self.position_label.configure(text=f'{secs}/{total_secs}')


PAD = '0.75m'
PROGRESS_WIDTH = 10

ADD_ICON = 'add.png'
CONFIG_ICON = 'config.png'
FILENEW_ICON = 'filenew.png'
FILEOPEN_ICON = 'fileopen.png'
