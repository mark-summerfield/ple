#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import tkinter as tk
import tkinter.ttk as ttk

import ActionMixin
import Config
import Player
import playlist
import UiMixin
from Const import INFO_FG, PAD, WARN_FG


class Window(ttk.Frame, UiMixin.UiMixin, ActionMixin.ActionMixin):

    def __init__(self, master, imagepath):
        super().__init__(master, padding=PAD)
        self.images = {}
        self.startup = True
        self.playing = None
        self.tracks = None # playlist.Playlist
        config = Config.config
        self.music_path = config.music_path
        self.deleted_track = None # for Undelete
        self.deleted_index = -1 # for Undelete
        self.status_timer_id = None
        self.playing_timer_id = None
        self.track_data_timer_id = None
        self.volume_var = tk.DoubleVar(value=config.current_volume)
        self.volume_var.trace_add('write', self.update_volume)
        self.position_var = tk.DoubleVar()
        self.make_images(imagepath)
        self.make_widgets()
        self.make_layout()
        self.make_bindings()
        self.initialize()
        self.playlists_pane.treeview.focus_set()


    def initialize(self):
        config = Config.config
        if config.current_playlist:
            self.playlists_pane.treeview.select(config.current_playlist)
        else:
            self.playlists_pane.focus_first_child()
        self.update_ui()
        if Player.player.valid:
            Player.player.volume = config.current_volume
            self.set_status_message('Ready')
        else:
            self.set_status_message('Playback unsupported: did not find a '
                                    'usable player library', fg=WARN_FG)


    def update_ui(self, _event=None):
        widgets = [self.add_button, self.edit_button, self.move_up_button,
                   self.move_down_button, self.remove_button,
                   self.unremove_button]
        if Player.player.valid:
            widgets += [self.previous_button, self.play_pause_button,
                        self.next_button, self.position_label,
                        self.position_progressbar, self.volume_label,
                        self.volume_scale]
        state = tk.DISABLED
        if self.tracks is not None:
            state = '!' + state
        for widget in widgets:
            widget.state([state])
        if self.deleted_track is None:
            self.unremove_button.state([tk.DISABLED])


    def set_status_message(self, message, *, millisec=10_000, fg=INFO_FG):
        if self.status_timer_id is not None:
            self.after_cancel(self.status_timer_id)
            self.status_timer_id = None
        self.status_label.configure(text=message, foreground=fg)
        if millisec:
            self.status_timer_id = self.after(
                millisec, lambda: self.status_label.config(text=''))


    def set_progress(self, secs, total_secs):
        if Player.player.valid:
            secs = playlist.humanized_length(secs)
            total_secs = playlist.humanized_length(total_secs)
            self.position_label.configure(text=f'{secs}/{total_secs}')


    def update_volume(self, *_):
        if Player.player.valid:
            volume = self.volume_var.get()
            Player.player.volume = volume
            self.volume_label.configure(text=f'Volume {volume * 100:.0f}%')


    def on_close(self, _event=None):
        config = Config.config
        config.current_playlist = self.playlists_pane.treeview.focus()
        config.current_track = self.a_playlist_pane.treeview.focus()
        if Player.player.valid:
            config.current_volume = Player.player.volume
        config.geometry = self.winfo_toplevel().geometry()
        self.quit()
