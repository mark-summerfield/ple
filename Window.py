#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import tkinter as tk
import tkinter.ttk as ttk

import ActionMixin
import Config
import Const
import Player
import playlist
import UiMixin


class Window(ttk.Frame, UiMixin.UiMixin, ActionMixin.ActionMixin):

    def __init__(self, master):
        super().__init__(master, padding=UiMixin.PAD)
        self.images = {}
        self.tracks = None # playlist.Playlist
        self.deleted_track = None # for Undelete
        self.deleted_index = -1 # for Undelete
        self.status_timer_id = None
        self.make_images()
        self.make_widgets()
        self.make_layout()
        self.make_bindings()
        self.playlists_pane.set_focus()
        self.update_ui()
        if Player.player.valid:
            self.set_status_message('Ready')
        else:
            self.set_status_message('Playback unsupported: did not find a '
                                    'usable player library',
                                    fg=Const.WARN_FG)


    def update_ui(self, _event=None):
        widgets = [self.add_button, self.edit_button, self.move_up_button,
                   self.move_down_button, self.remove_button,
                   self.unremove_button]
        if Player.player.valid:
            widgets += [self.previous_button, self.play_pause_button,
                        self.next_button, self.volume_label,
                        self.volume_spinbox, self.position_label,
                        self.position_progress]
        state = tk.DISABLED
        if self.tracks is not None:
            state = '!' + state
        for widget in widgets:
            widget.state([state])
        # NOTE set_progress() ?


    def set_status_message(self, message, *, millisec=10_000,
                           fg=Const.INFO_FG):
        if self.status_timer_id is not None:
            self.after_cancel(self.status_timer_id)
            self.status_timer_id = None
        self.status_label.configure(text=message, foreground=fg)
        if millisec:
            self.status_timer_id = self.after(
                millisec, lambda: self.status_label.config(text=''))


    def set_progress(self, secs, total_secs):
        if Player.player.valid:
            size = round((secs / total_secs) * UiMixin.PROGRESS_WIDTH)
            text = ('▉' * size) + ('▕' * (UiMixin.PROGRESS_WIDTH - size))
            self.position_progress.configure(text=text)
            secs = playlist.humanized_length(secs)
            total_secs = playlist.humanized_length(total_secs)
            self.position_label.configure(text=f'{secs}/{total_secs}')


    def on_close(self, _event=None):
        Config.config.geometry = self.winfo_toplevel().geometry()
        self.quit()
