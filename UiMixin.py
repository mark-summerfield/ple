#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3


import pathlib
import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

import Config
import Player
import PlaylistPane
import PlaylistsPane
import Tooltip
from Const import APPNAME, NS, NSWE, PAD, WE


class UiMixin:

    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (ABOUT_ICON, ADD_ICON, CONFIG_ICON, EDIT_ICON,
                     FILENEW_ICON, FILEOPEN_ICON, HELP_ICON, MOVE_DOWN_ICON,
                     MOVE_UP_ICON, NEXT_ICON, PAUSE_ICON, PLAY_ICON,
                     PREVIOUS_ICON, QUIT_ICON, REMOVE_ICON, UNREMOVE_ICON):
            self.images[name] = tk.PhotoImage(file=path / name)


    def make_widgets(self):
        self.make_main_buttons()
        self.splitter = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.playlists_pane = PlaylistsPane.PlaylistsPane(
            self.splitter, path=Config.config.playlists_path)
        self.a_playlist_pane = PlaylistPane.PlaylistPane(self.splitter)
        self.make_playlist_buttons()
        if Player.player.valid:
            self.make_player_buttons()
            self.make_scales()
        self.status_label = ttk.Label(self.master, foreground='navy',
                                      relief=tk.SUNKEN)


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
                        f'Configure {APPNAME} • Ctrl+C')
        self.about_button = ttk.Button(
            self.button_frame, text='About', takefocus=False, underline=1,
            image=self.images[ABOUT_ICON], command=self.on_about,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.about_button,
                        f'About {APPNAME} • Ctrl+B')
        self.help_button = ttk.Button(
            self.button_frame, text='Help', takefocus=False, underline=0,
            image=self.images[HELP_ICON], command=self.on_help,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.help_button, 'Show Help • F1')
        self.quit_button = ttk.Button(
            self.button_frame, text='Quit', takefocus=False, underline=0,
            image=self.images[QUIT_ICON], command=self.on_close,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.quit_button,
                        f'Quit {APPNAME} • Esc or Ctrl+Q')


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
        self.player_frame = ttk.Frame(self.playlist_button_frame)
        self.previous_button = ttk.Button(
            self.player_frame, takefocus=False,
            image=self.images[PREVIOUS_ICON],
            command=self.on_previous_track)
        Tooltip.Tooltip(self.previous_button,
                        'Start Playing Previous Track • Ctrl+S')
        self.play_pause_button = ttk.Button(
            self.player_frame, takefocus=False,
            image=self.images[PLAY_ICON],
            command=self.on_play_or_pause_track)
        Tooltip.Tooltip(self.play_pause_button,
                        'Play or Pause the Current Track • Ctrl+P')
        self.next_button = ttk.Button(
            self.player_frame, takefocus=False,
            image=self.images[NEXT_ICON], command=self.on_next_track)
        Tooltip.Tooltip(self.next_button,
                        'Start Playing Next Track • Ctrl+T')


    def make_scales(self):
        self.volume_label = ttk.Label(self.player_frame, text='Volume',
                                      underline=0, anchor=tk.CENTER)
        self.volume_spinbox = ttk.Spinbox(
            self.player_frame, from_=0, to=100, wrap=False,
            format='%3.0f%%', width=5, justify=tk.RIGHT)
        self.volume_spinbox.set('50%')
        self.position_label = ttk.Label(self.player_frame, text='0″/0″',
                                        anchor=tk.CENTER)
        self.position_progress = ttk.Label(
            self.player_frame, relief=tk.SUNKEN, width=PROGRESS_WIDTH,
            foreground='#8080FF', background='#FFFFCD',
            font=tkfont.nametofont('TkFixedFont'))


    def make_layout(self):
        self.make_main_button_layout()
        common = dict(padx=PAD, pady=PAD, sticky=NSWE)
        self.playlists_pane.grid(row=0, column=0, **common)
        self.a_playlist_pane.grid(row=0, column=1, **common)
        self.splitter.add(self.playlists_pane, weight=1)
        self.splitter.add(self.a_playlist_pane, weight=3)
        self.splitter.grid(row=0, column=1, columnspan=2, rowspan=2,
                           sticky=NSWE)
        self.make_playlist_button_layout()
        if Player.player.valid:
            self.make_player_layout()
            self.make_scales_layout()
        self.playlist_button_frame.grid(row=0, column=3, padx=PAD, pady=PAD,
                                        sticky=NS)
        self.status_label.grid(row=2, column=0, columnspan=4, padx=PAD,
                               pady=PAD, sticky=WE)
        top = self.winfo_toplevel()
        top.columnconfigure(1, weight=1)
        top.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)


    def make_main_button_layout(self):
        common = dict(column=0, sticky=WE, pady=PAD, padx=PAD)
        self.file_new_button.grid(row=0, **common)
        self.folder_open_button.grid(row=1, **common)
        self.config_button.grid(row=2, **common)
        self.about_button.grid(row=3, **common)
        self.help_button.grid(row=4, **common)
        self.quit_button.grid(row=6, **common)
        self.button_frame.rowconfigure(5, weight=1)
        self.button_frame.grid(row=0, column=0, padx=PAD, pady=PAD,
                               sticky=NS)


    def make_playlist_button_layout(self):
        common = dict(sticky=WE, pady=PAD, padx=PAD)
        self.add_button.grid(row=0, **common)
        self.edit_button.grid(row=1, **common)
        self.move_up_button.grid(row=2, **common)
        self.move_down_button.grid(row=3, **common)
        self.remove_button.grid(row=4, **common)
        self.unremove_button.grid(row=5, **common)


    def make_player_layout(self):
        common = dict(sticky=WE, pady=PAD, padx=PAD)
        self.player_frame.grid(row=7, **common)
        self.previous_button.grid(row=0, column=0, **common)
        self.play_pause_button.grid(row=0, column=1, **common)
        self.next_button.grid(row=0, column=2, **common)
        self.playlist_button_frame.rowconfigure(6, weight=1)


    def make_scales_layout(self):
        common = dict(sticky=WE, pady=PAD, padx=PAD, column=0, columnspan=3)
        self.volume_label.grid(row=1, **common)
        self.volume_spinbox.grid(row=2, sticky=tk.S, pady=PAD, padx=PAD,
                                 column=0, columnspan=3)
        self.position_label.grid(row=3, **common)
        self.position_progress.grid(row=4, **common)


    def make_bindings(self):
        self.a_playlist_pane.treeview.bind('<Double-Button-1>',
                                           self.on_edit_track)
        self.a_playlist_pane.treeview.bind('<Return>', self.on_edit_track)
        self.playlists_pane.treeview.bind('<<TreeviewSelect>>',
                                          self.on_playlists_select)
        self.master.bind('<F1>', self.on_help)
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
        self.master.bind('<Control-h>', self.on_help)
        self.master.bind('<Alt-h>', self.on_help)
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
        self.a_playlist_pane.treeview.bind('<space>',
                                           self.on_play_or_pause_track)
        self.master.bind('<Control-p>', self.on_play_or_pause_track)
        self.master.bind('<Control-s>', self.on_previous_track)
        self.master.bind('<Control-t>', self.on_next_track)
        self.master.bind('<Alt-v>',
                         lambda *_: self.volume_spinbox.focus_set())


PROGRESS_WIDTH = 12

ABOUT_ICON = 'help-about.png'
ADD_ICON = 'list-add.png'
CONFIG_ICON = 'document-properties.png'
EDIT_ICON = 'stock_edit.png'
FILENEW_ICON = 'filenew.png'
FILEOPEN_ICON = 'fileopen.png'
HELP_ICON = 'help-contents.png'
MOVE_DOWN_ICON = 'go-next.png'
MOVE_UP_ICON = 'go-previous.png'
NEXT_ICON = 'media-seek-forward.png'
PAUSE_ICON = 'media-playback-pause.png'
PLAY_ICON = 'media-playback-start.png'
PREVIOUS_ICON = 'media-seek-backward.png'
QUIT_ICON = 'exit.png'
REMOVE_ICON = 'list-remove.png'
UNREMOVE_ICON = 'edit-undo.png'
