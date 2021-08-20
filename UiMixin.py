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
from Const import APPNAME, NS, NSWE, PAD, PAUSE_ICON, PLAY_ICON, WE


class UiMixin:

    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (ABOUT_ICON, ADD_ICON, EDIT_ICON, FILENEW_ICON,
                     HELP_ICON, MOVE_DOWN_ICON, MOVE_UP_ICON, NEXT_ICON,
                     PAUSE_ICON, PLAY_ICON, PREVIOUS_ICON, QUIT_ICON,
                     REMOVE_ICON, UNREMOVE_ICON):
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
        self.about_button = ttk.Button(
            self.button_frame, text='About', takefocus=False, underline=1,
            image=self.images[ABOUT_ICON], command=self.on_about,
            compound=tk.LEFT)
        Tooltip.Tooltip(self.about_button, f'About {APPNAME} • Ctrl+B')
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
                        'Start Playing Previous Track • Ctrl+P')
        self.play_pause_button = ttk.Button(
            self.player_frame, takefocus=False,
            image=self.images[PLAY_ICON],
            command=self.on_play_or_pause_track)
        Tooltip.Tooltip(self.play_pause_button,
                        'Play or Pause the Current Track • Spacebar')
        self.next_button = ttk.Button(
            self.player_frame, takefocus=False,
            image=self.images[NEXT_ICON], command=self.on_next_track)
        Tooltip.Tooltip(self.next_button,
                        'Start Playing Next Track • Ctrl+T')


    def make_scales(self):
        font = tkfont.nametofont('TkFixedFont')
        yellow = '#FFFFCD'
        self.volume_label = ttk.Label(self.player_frame, text='Volume',
                                      anchor=tk.CENTER)
        self.volume_frame = ttk.Frame(self.player_frame)
        self.volume_label_mute = ttk.Label(
            self.volume_frame, width=1, font=font, foreground='navy',
            background=yellow, relief=tk.SUNKEN)
        self.volume_label_mid = ttk.Label(
            self.volume_frame, width=PROGRESS_WIDTH - 2, font=font,
            foreground='#8080FF', background=yellow, relief=tk.SUNKEN)
        self.volume_label_max = ttk.Label(
            self.volume_frame, width=1, font=font, foreground='#FF8080',
            background=yellow, relief=tk.SUNKEN)
        self.position_label = ttk.Label(self.player_frame, text='0″/0″',
                                        anchor=tk.CENTER)
        self.position_progress = ttk.Label(
            self.player_frame, relief=tk.SUNKEN, width=PROGRESS_WIDTH,
            foreground='#80FF80', background=yellow, font=font)


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
        self.about_button.grid(row=1, **common)
        self.help_button.grid(row=2, **common)
        self.quit_button.grid(row=4, **common)
        self.button_frame.rowconfigure(3, weight=1)
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
        self.previous_button.grid(row=2, column=0, **common)
        self.play_pause_button.grid(row=2, column=1, **common)
        self.next_button.grid(row=2, column=2, **common)
        self.playlist_button_frame.rowconfigure(6, weight=1)


    def make_scales_layout(self):
        common = dict(sticky=WE, pady=PAD, padx=PAD, column=0, columnspan=3)
        self.volume_label.grid(row=0, **common)
        self.volume_frame.grid(row=1, **common)
        self.volume_label_mute.grid(row=0, column=0, ipadx=PAD, pady=PAD)
        self.volume_label_mid.grid(row=0, column=1, ipadx=PAD, pady=PAD,
                                   sticky=WE)
        self.volume_label_max.grid(row=0, column=2, ipadx=PAD, pady=PAD)
        self.position_label.grid(row=3, **common)
        self.position_progress.grid(row=4, **common)


    def make_bindings(self):
        self.a_playlist_pane.treeview.bind('<Double-Button-1>',
                                           self.on_edit_track)
        self.a_playlist_pane.treeview.bind('<Return>', self.on_edit_track)
        self.playlists_pane.treeview.bind('<<TreeviewSelect>>',
                                          self.on_playlists_select)
        self.master.bind('<F1>', lambda *_: self.help_button.invoke())
        self.master.bind('<Escape>', lambda *_: self.quit_button.invoke())
        self.master.bind('<Alt-a>', lambda *_: self.add_button.invoke())
        self.master.bind('<Control-a>', lambda *_: self.add_button.invoke())
        self.master.bind('<Alt-b>', lambda *_: self.about_button.invoke())
        self.master.bind('<Control-b>',
                         lambda *_: self.about_button.invoke())
        self.master.bind('<Alt-d>',
                         lambda *_: self.move_down_button.invoke())
        self.master.bind('<Control-d>',
                         lambda *_: self.move_down_button.invoke())
        self.master.bind('<Alt-e>',
                         lambda *_: self.edit_button.invoke())
        self.master.bind('<Control-e>',
                         lambda *_: self.edit_button.invoke())
        self.master.bind('<Alt-h>', lambda *_: self.help_button.invoke())
        self.master.bind('<Control-h>',
                         lambda *_: self.help_button.invoke())
        self.master.bind('<Alt-m>',
                         lambda *_: self.unremove_button.invoke())
        self.master.bind('<Control-m>',
                         lambda *_: self.unremove_button.invoke())
        self.master.bind('<Alt-n>',
                         lambda *_: self.file_new_button.invoke())
        self.master.bind('<Control-n>',
                         lambda *_: self.file_new_button.invoke())
        self.master.bind('<Alt-q>', lambda *_: self.quit_button.invoke())
        self.master.bind('<Control-q>',
                         lambda *_: self.quit_button.invoke())
        self.master.bind('<Alt-r>', lambda *_: self.remove_button.invoke())
        self.master.bind('<Control-r>',
                         lambda *_: self.remove_button.invoke())
        self.master.bind('<Alt-u>', lambda *_: self.move_up_button.invoke())
        self.master.bind('<Control-u>',
                         lambda *_: self.move_up_button.invoke())
        if Player.player.valid:
            self.make_player_bindings()


    def make_player_bindings(self):
        self.master.bind('<space>',
                         lambda *_: self.play_pause_button.invoke())
        self.master.bind('<Control-p>',
                         lambda *_: self.previous_button.invoke())
        self.master.bind('<Control-t>',
                         lambda *_: self.next_button.invoke())


PROGRESS_WIDTH = 12

ABOUT_ICON = 'help-about.png'
ADD_ICON = 'list-add.png'
EDIT_ICON = 'stock_edit.png'
FILENEW_ICON = 'filenew.png'
HELP_ICON = 'help-contents.png'
MOVE_DOWN_ICON = 'go-next.png'
MOVE_UP_ICON = 'go-previous.png'
NEXT_ICON = 'media-seek-forward.png'
PREVIOUS_ICON = 'media-seek-backward.png'
QUIT_ICON = 'exit.png'
REMOVE_ICON = 'list-remove.png'
UNREMOVE_ICON = 'edit-undo.png'
