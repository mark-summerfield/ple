#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import os

import AboutForm
import playlist


class ActionMixin:

    def on_playlists_select(self, _event=None):
        self.a_playlist_pane.clear()
        name = self.playlists_pane.treeview.focus()
        if name:
            if os.path.isdir(name):
                self.tracks = None
                count = 0
                for _, _, files in os.walk(name):
                    for file in files:
                        if playlist.is_playlist(file):
                            count += 1
                if count == 0:
                    message = name
                elif count == 1:
                    message = f'One playlist in {name}'
                else:
                    message = f'{count:,} playlists in {name}'
                self.set_status_message(message)
            elif playlist.is_playlist(name):
                self.tracks = playlist.Playlist(name)
                self.set_status_message(
                    f'{len(self.tracks):,} tracks in {name}')
                self.a_playlist_pane.set_tracks(self.tracks)
            self.update_ui()


    def on_new_playlist(self, _event=None):
        print('on_new_playlist')


    def on_folder_open(self, _event=None):
        print('on_folder_open')


    def on_config(self, _event=None):
        print('on_config')


    def on_about(self, _event=None):
        AboutForm.Form(self)


    def on_add_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_add_track')


    def on_edit_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_edit_track')


    def on_move_track_up(self, _event=None):
        if self.tracks is None:
            return
        print('on_move_track_up')


    def on_move_track_down(self, _event=None):
        if self.tracks is None:
            return
        print('on_move_track_down')


    def on_remove_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_remove_track')


    def on_unremove_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_unremove_track')


    def on_previous_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_previous_track')


    def on_play_or_pause_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_play_or_pause_track')


    def on_next_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_next_track')
