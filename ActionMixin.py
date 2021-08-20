#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import os
import tkinter.filedialog

import AboutForm
import Config
import HelpForm
import Player
import playlist
import TrackForm
from Const import APPNAME, ERROR_FG, PAUSE_ICON, PLAY_ICON


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
            if self.startup:
                self.a_playlist_pane.treeview.select(
                    Config.config.current_track)
                self.startup = False
        except (OSError, playlist.Error) as err:
            self.tracks = None
            self.set_status_message(f'Failed to load playlist: {err}',
                                    fg=ERROR_FG)


    def on_new_playlist(self, _event=None):
        path = tkinter.filedialog.askdirectory(
            parent=self, title=f'New Playlist — {APPNAME}',
            initialdir=self.music_path, mustexist=True)
        if path:
            playlist_name = self.populate_new_playlist(path)
            self.playlists_pane.set_path(Config.config.playlists_path)
            self.playlists_pane.treeview.select(playlist_name)


    def populate_new_playlist(self, path):
        playlist_name = self.unique_new_playlist_name(path)
        self.tracks = playlist.Playlist(playlist_name)
        for filename in playlist.filter(path):
            self.tracks += playlist.Track(
                playlist.normalize_name(filename), filename, -1)
        self.tracks.sort()
        return playlist_name


    def unique_new_playlist_name(self, path):
        config = Config.config
        playlists_path = config.playlists_path
        basename = os.path.basename(path)
        suffix = config.default_playlist_suffix.lower()
        count = 0
        while True:
            n = f'-{count}' if count else ''
            playlist_name = os.path.join(playlists_path,
                                         basename + n + suffix)
            if not os.path.exists(playlist_name):
                return playlist_name
            count += 1


    def on_about(self, _event=None):
        AboutForm.Form(self)


    def on_help(self, _event=None):
        HelpForm.Form(self)


    def on_add_track(self, _event=None):
        if self.tracks is None:
            return
        filename = tkinter.filedialog.askopenfilename(
            parent=self, title=f'Add Track — {APPNAME}',
            initialdir=self.music_path,
            filetypes=(('Ogg', '*.ogg'), ('Ogg audio', '*.oga'),
                       ('MP3', '*.mp3')))
        if filename:
            self.music_path = os.path.dirname(filename)
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
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            self.deleted_index = treeview.index(iid)
            focus_iid = treeview.next(iid)
            if not focus_iid:
                focus_iid = treeview.prev(iid)
            treeview.delete(iid)
            if focus_iid:
                treeview.select(focus_iid)
            self.deleted_track = self.tracks.pop(self.deleted_index)
            self.update_ui()


    def on_unremove_track(self, _event=None):
        if self.tracks is None or self.deleted_track is None:
            return
        self.tracks.insert(self.deleted_index, self.deleted_track)
        treeview = self.a_playlist_pane.treeview
        treeview.insert(
            '', self.deleted_index, iid=self.deleted_track.filename,
            text=self.deleted_track.title, image=self.a_playlist_pane.image)
        treeview.select(self.deleted_track.filename)
        self.deleted_track = None
        self.deleted_index = -1
        self.update_ui()


    def on_previous_track(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            prev_iid = treeview.prev(iid)
            if not prev_iid:
                return # Can't go before first one
            if self.playing:
                self.on_play_or_pause_track() # Pause/Stop
            treeview.select(prev_iid)
            self.on_play_or_pause_track() # Play


    def on_play_or_pause_track(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            if not self.playing:
                if iid == Player.player.filename:
                    Player.player.resume()
                else:
                    Player.player.play(iid)
                icon = PAUSE_ICON
                self.playing = True
                self.while_playing()
            else:
                Player.player.pause()
                icon = PLAY_ICON
                self.playing = False
            self.play_pause_button.config(image=self.images[icon])


    def on_next_track(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            next_iid = treeview.next(iid)
            if not next_iid:
                return # Can't go after last one
            if self.playing:
                self.on_play_or_pause_track() # Pause/Stop
            treeview.select(next_iid)
            self.on_play_or_pause_track() # Play


    def while_playing(self, _event=None):
        if self.playing:
            self.set_progress(Player.player.pos, Player.player.length)
            self.playing_timer_id = self.after(1000, self.while_playing)
        elif self.playing_timer_id is not None:
            self.after_cancel(self.playing_timer_id)
            self.playing_timer_id = None
