#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import os
import tkinter.filedialog

import AboutForm
import Config
import HelpForm
import playlist
import TrackForm
from Const import APPNAME, ERROR_FG


class ActionMixin:

    def on_playlists_select(self, _event=None):
        self.a_playlist_pane.clear()
        name = self.playlists_pane.treeview.focus()
        if name:
            if os.path.isdir(name):
                self.folder_selected(name)
            elif playlist.is_playlist(name):
                self.playlist_selected(name)
            self.update_ui()


    def folder_selected(self, name):
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


    def playlist_selected(self, name):
        try:
            self.tracks = playlist.Playlist(name)
            self.set_status_message(
                f'{len(self.tracks):,} tracks in {name}', millisec=None)
            self.a_playlist_pane.set_tracks(self.tracks)
        except (OSError, playlist.Error) as err:
            self.tracks = None
            self.set_status_message(f'Failed to load playlist: {err}',
                                    fg=ERROR_FG)


    def on_new_playlist(self, _event=None):
        print('on_new_playlist') # TODO
        # TODO user chooses music folder
        # TODO create unique playlist name based on the music folder's name
        # in the playlist folder dir (adding -1 or -2 ... if needed to avoid
        # clobbering an existing playlist)
        # TODO iterate music folder using playlist.filter(music_folder) and
        # add tracks using playlist.Track(playlist.normalize_name(...


    def on_about(self, _event=None):
        AboutForm.Form(self)


    def on_help(self, _event=None):
        HelpForm.Form(self)


    def on_add_track(self, _event=None):
        if self.tracks is None:
            return
        config = Config.config
        path = (config.music_path if self.music_path is None else
                self.music_path)
        filename = tkinter.filedialog.askopenfilename(
            parent=self, title=f'Add Track — {APPNAME}', initialdir=path,
            filetypes=(('Ogg', '*.ogg'), ('Ogg audio', '*.oga'),
                       ('MP3', '*.mp3')))
        if filename:
            track = playlist.Track(playlist.normalize_name(filename),
                                   filename, -1)
            self.tracks += track
            self.a_playlist_pane.append(track)
            self.a_playlist_pane.treeview.select(filename)


    def on_edit_track(self, _event=None):
        if self.tracks is None:
            return
        track = None
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            index = treeview.index(iid)
            if index > -1:
                track = self.tracks[index]
                form = TrackForm.Form(self, track)
                if form.edited_track is not None:
                    parent = treeview.parent(iid)
                    treeview.delete(iid)
                    treeview.insert(
                        parent, index, iid=form.edited_track.filename,
                        text=form.edited_track.title,
                        image=self.a_playlist_pane.image)
                    self.tracks[index] = form.edited_track
            treeview.focus_set()
            treeview.select(iid)


    def on_move_track_up(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            index = treeview.index(iid)
            if self.tracks.moveup(index):
                treeview.move(iid, '', index - 1)


    def on_move_track_down(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            index = treeview.index(iid)
            if self.tracks.movedown(index):
                treeview.move(iid, '', index + 1)


    def on_remove_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_remove_track') # TODO


    def on_unremove_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_unremove_track') # TODO


    def on_previous_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_previous_track') # TODO


    def on_play_or_pause_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_play_or_pause_track') # TODO


    def on_next_track(self, _event=None):
        if self.tracks is None:
            return
        print('on_next_track') # TODO
