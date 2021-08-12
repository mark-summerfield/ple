#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3


import pathlib
import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

import Config
import Const
import Player
import PlaylistPane
import PlaylistsPane
import Tooltip


class UiMixin:

    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (ABOUT_ICON, ADD_ICON, CONFIG_ICON, EDIT_ICON,
                     FILENEW_ICON, FILEOPEN_ICON, MOVE_DOWN_ICON,
                     MOVE_UP_ICON, NEXT_ICON, PAUSE_ICON, PLAY_ICON,
                     PREVIOUS_ICON, QUIT_ICON, REMOVE_ICON, UNREMOVE_ICON):
            self.images[name] = tk.PhotoImage(file=path / name)


    def make_widgets(self):
        self.make_main_buttons()
        self.playlists_pane = PlaylistsPane.PlaylistsPane(
            self.master, padding=PAD, path=Config.config.playlists_path)
        self.a_playlist_pane = PlaylistPane.PlaylistPane(self.master,
                                                         padding=PAD)
        self.make_playlist_buttons()
        if Player.player.valid:
            self.make_player_buttons()
            self.make_scales()


    def make_main_buttons(self):
        self.button_frame = ttk.Frame(self.master)
        self.file_new_button = ttk.Button(
            self.button_frame, text='New', underline=0, takefocus=False,
            image=self.images[FILENEW_ICON], command=self.on_new_playlist,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.file_new_button,
                        'Create New Playlist • Ctrl+N')
        self.folder_open_button = ttk.Button(
            self.button_frame, text='Open', underline=0, takefocus=False,
            image=self.images[FILEOPEN_ICON], command=self.on_folder_open,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.folder_open_button,
                        'Open Playlist Folder • Ctrl+O')
        self.config_button = ttk.Button(
            self.button_frame, text='Config', underline=0, takefocus=False,
            image=self.images[CONFIG_ICON], command=self.on_config,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.config_button,
                        f'Configure {Const.APPNAME} • Ctrl+C')
        self.about_button = ttk.Button(
            self.button_frame, text='About', takefocus=False, underline=1,
            image=self.images[ABOUT_ICON], command=self.on_about,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.about_button,
                        f'About {Const.APPNAME} • Ctrl+B')
        self.quit_button = ttk.Button(
            self.button_frame, text='Quit', takefocus=False, underline=0,
            image=self.images[QUIT_ICON], command=self.on_close,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.quit_button,
                        f'Quit {Const.APPNAME} • Esc or Ctrl+Q')


    def make_playlist_buttons(self):
        self.playlist_button_frame = ttk.Frame(self.master)
        self.add_button = ttk.Button(
            self.playlist_button_frame, text='Add', underline=0,
            takefocus=False, image=self.images[ADD_ICON],
            command=self.on_add_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.add_button, 'Add Track to Playlist • Ctrl+A')
        self.edit_button = ttk.Button(
            self.playlist_button_frame, text='Edit', underline=0,
            takefocus=False, image=self.images[EDIT_ICON],
            command=self.on_edit_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.edit_button, 'Edit Track\'s Name • Ctrl+E')
        self.move_up_button = ttk.Button(
            self.playlist_button_frame, text='Move Up', underline=5,
            takefocus=False, image=self.images[MOVE_UP_ICON],
            command=self.on_move_track_up, compound=tk.LEFT)
        Tooltip.Tooltip(self.move_up_button, 'Move Track Up • Ctrl+U')
        self.move_down_button = ttk.Button(
            self.playlist_button_frame, text='Move Down', underline=5,
            takefocus=False, image=self.images[MOVE_DOWN_ICON],
            command=self.on_move_track_down, compound=tk.LEFT)
        Tooltip.Tooltip(self.move_down_button, 'Move Track Down • Ctrl+D')
        self.remove_button = ttk.Button(
            self.playlist_button_frame, text='Remove', underline=0,
            takefocus=False, image=self.images[REMOVE_ICON],
            command=self.on_remove_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.remove_button, 'Remove Track • Ctrl+R')
        self.unremove_button = ttk.Button(
            self.playlist_button_frame, text='Unremove', underline=4,
            takefocus=False, image=self.images[UNREMOVE_ICON],
            command=self.on_unremove_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.unremove_button,
                        'Unremove Last Removed Track • Ctrl+M')


    def make_player_buttons(self):
        self.previous_button = ttk.Button(
            self.playlist_button_frame, text='Previous', underline=7,
            takefocus=False, image=self.images[PREVIOUS_ICON],
            command=self.on_previous_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.previous_button,
                        'Start Playing Previous Track • Ctrl+S')
        self.play_pause_button = ttk.Button(
            self.playlist_button_frame, text='Play', underline=0,
            takefocus=False, image=self.images[PLAY_ICON],
            command=self.on_play_or_pause_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.play_pause_button,
                        'Play or Pause the Current Track • Ctrl+P')
        self.next_button = ttk.Button(
            self.playlist_button_frame, text='Next', underline=3,
            takefocus=False, image=self.images[NEXT_ICON],
            command=self.on_next_track, compound=tk.LEFT)
        Tooltip.Tooltip(self.next_button,
                        'Start Playing Next Track • Ctrl+T')


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
            font=tkfont.nametofont('TkFixedFont'))


    def make_layout(self):
        self.make_main_button_layout()
        self.playlists_pane.grid(
            row=0, column=1, rowspan=2, padx=PAD, pady=PAD,
            sticky=tk.W + tk.E + tk.N + tk.S)
        self.a_playlist_pane.grid(
            row=0, column=2, rowspan=2, padx=PAD, pady=PAD,
            sticky=tk.W + tk.E + tk.N + tk.S)
        self.make_playlist_button_layout()
        if Player.player.valid:
            self.make_player_layout()
            self.make_scales_layout()
        self.playlist_button_frame.grid(row=0, column=3, padx=PAD, pady=PAD,
                                        sticky=tk.N + tk.S)
        top = self.winfo_toplevel()
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        top.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)


    def make_main_button_layout(self):
        common = dict(column=0, sticky=tk.W + tk.E, pady=PAD, padx=PAD)
        self.file_new_button.grid(row=0, **common)
        self.folder_open_button.grid(row=1, **common)
        self.config_button.grid(row=2, **common)
        self.about_button.grid(row=3, **common)
        self.quit_button.grid(row=5, **common)
        self.button_frame.rowconfigure(4, weight=1)
        self.button_frame.grid(row=0, column=0, padx=PAD, pady=PAD,
                               sticky=tk.N + tk.S)


    def make_playlist_button_layout(self):
        common = dict(sticky=tk.W + tk.E, pady=PAD, padx=PAD)
        self.add_button.grid(row=0, **common)
        self.edit_button.grid(row=1, **common)
        self.move_up_button.grid(row=2, **common)
        self.move_down_button.grid(row=3, **common)
        self.remove_button.grid(row=4, **common)
        self.unremove_button.grid(row=5, **common)


    def make_player_layout(self):
        common = dict(sticky=tk.W + tk.E, pady=PAD, padx=PAD)
        self.previous_button.grid(row=7, **common)
        self.play_pause_button.grid(row=8, **common)
        self.next_button.grid(row=9, **common)
        self.playlist_button_frame.rowconfigure(6, weight=1)


    def make_scales_layout(self):
        self.volume_label.grid(row=0, column=0, padx=PAD, pady=PAD,
                               sticky=tk.S)
        self.volume_spinbox.grid(row=1, column=0, padx=PAD, pady=PAD,
                                 sticky=tk.S)
        self.volume_frame.grid(row=1, column=0, padx=PAD, pady=PAD,
                               sticky=tk.S)
        self.position_label.grid(row=0, column=0, padx=PAD, pady=PAD,
                                 sticky=tk.S)
        self.position_progress.grid(row=1, column=0, padx=PAD, pady=PAD,
                                    sticky=tk.S)
        self.position_frame.grid(row=1, column=3, padx=PAD, pady=PAD,
                                 sticky=tk.S)


    def make_bindings(self):
        self.master.bind('<Escape>', self.on_close)
        self.master.bind('<Alt-a>', self.on_add_track)
        self.master.bind('<Control-a>', self.on_add_track)
        self.master.bind('<Alt-b>', self.on_about)
        self.master.bind('<Control-b>', self.on_about)
        self.master.bind('<Alt-c>', self.on_config)
        self.master.bind('<Control-c>', self.on_config)
        self.master.bind('<Alt-d>', self.on_move_track_down)
        self.master.bind('<Control-d>', self.on_move_track_down)
        self.master.bind('<Alt-e>', self.on_edit_track)
        self.master.bind('<Control-e>', self.on_edit_track)
        self.master.bind('<Alt-m>', self.on_unremove_track)
        self.master.bind('<Control-m>', self.on_unremove_track)
        self.master.bind('<Alt-n>', self.on_new_playlist)
        self.master.bind('<Control-n>', self.on_new_playlist)
        self.master.bind('<Alt-o>', self.on_folder_open)
        self.master.bind('<Control-o>', self.on_folder_open)
        self.master.bind('<Alt-q>', self.on_close)
        self.master.bind('<Control-q>', self.on_close)
        self.master.bind('<Alt-r>', self.on_remove_track)
        self.master.bind('<Control-r>', self.on_remove_track)
        self.master.bind('<Alt-u>', self.on_move_track_up)
        self.master.bind('<Control-u>', self.on_move_track_up)
        if Player.player.valid:
            self.make_player_bindings()


    def make_player_bindings(self):
        self.master.bind('<Alt-p>', self.on_play_or_pause_track)
        self.master.bind('<Control-p>', self.on_play_or_pause_track)
        self.master.bind('<Alt-s>', self.on_previous_track)
        self.master.bind('<Control-s>', self.on_previous_track)
        self.master.bind('<Alt-t>', self.on_next_track)
        self.master.bind('<Control-t>', self.on_next_track)
        self.master.bind('<Alt-v>',
                         lambda *_: self.volume_spinbox.focus_set())


PAD = '0.75m'
PROGRESS_WIDTH = 12

ABOUT_ICON = 'help-about.png'
ADD_ICON = 'list-add.png'
CONFIG_ICON = 'document-properties.png'
EDIT_ICON = 'edit-select-all.png'
FILENEW_ICON = 'filenew.png'
FILEOPEN_ICON = 'fileopen.png'
MOVE_DOWN_ICON = 'go-next.png'
MOVE_UP_ICON = 'go-previous.png'
NEXT_ICON = 'media-seek-forward.png'
PAUSE_ICON = 'media-playback-pause.png'
PLAY_ICON = 'media-playback-start.png'
PREVIOUS_ICON = 'media-seek-backward.png'
QUIT_ICON = 'exit.png'
REMOVE_ICON = 'list-remove.png'
UNREMOVE_ICON = 'edit-undo.png'
