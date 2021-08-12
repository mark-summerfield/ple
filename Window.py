#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

# TODO in order:
'''
Show Playlist: when the user navigates to a playlist show it in the Playlist
view and set self.playlist to Playlist(filename) then call self.update_ui()

New: create new empty playlist with a *filename*
Add: add one or more new tracks to the current playlist
Edit: rename the title of the current track in the current playlist
Move Up: move the current track up one in the current playlist
Move Down: move the current track down one in the current playlist
Remove: delete the current track from the current playlist
Unremove: undelete the most recently deleted track from the current playlist
Prev: only show if default player is PLE
Play|Pause: if default player is external then only show [>] Play and
            when clicked send the current track to the player; if the track
            plays to the end automatically makes the next track current and
            starts playing it and so on until the end of the playlist
Next: only show if default player is PLE
volume: volume slider 0..100%
position: progress slider MmSs/MmSs

Open: open folder
Config: default music folder; default playlists folder
'''

import tkinter as tk
import tkinter.ttk as ttk

import Config
import DataMixin
import Player
import playlist
import UiMixin


class Window(ttk.Frame, UiMixin.UiMixin, DataMixin.DataMixin):

    def __init__(self, master):
        super().__init__(master, padding=UiMixin.PAD)
        self.images = {}
        self.tracks = None # playlist.Playlist
        self.deleted_track = None # for Undelete
        self.deleted_index = -1 # for Undelete
        self.make_images()
        self.make_widgets()
        self.make_layout()
        self.make_bindings()
        self.playlists_pane.set_focus()
        self.update_ui()


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
