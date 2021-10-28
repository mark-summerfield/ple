#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import math
import os
import tkinter.filedialog

import AboutForm
import Config
import HelpForm
import Player
import playlist
import TrackForm
from Const import APPNAME, ERROR_FG, PAUSE_ICON, PLAY_ICON, VERSION


class ActionMixin:

    __slots__ = ()

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
            self.a_playlist_pane.set_tracks(self.tracks)
            if self.startup:
                self.a_playlist_pane.treeview.select(
                    Config.config.current_track)
                self.startup = False
            self.set_status_message(
                f'{len(self.tracks):,} tracks in {name} of '
                f'{self.tracks.humanized_length}', millisec=None)
            if self.playing is None:
                self.maybe_update_times(name)
            else:
                treeview = self.a_playlist_pane.treeview
                if treeview.exists(self.playing):
                    text = treeview.item(self.playing, 'text')
                    i = text.find('•')
                    if i > -1:
                        text = text[:i].rstrip()
                    self.set_status_message(text, millisec=None)
                    treeview.select(self.playing)
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
        self.focus_set()


    def populate_new_playlist(self, path):
        playlist_name = self.unique_new_playlist_name(path)
        self.tracks = playlist.Playlist(playlist_name)
        for filename in playlist.filter(path):
            self.tracks += playlist.Track(playlist.normalize_name(filename),
                                          filename)
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


    def on_options(self, _event=None):
        print('on_options')


    def on_about(self, _event=None):
        AboutForm.Form(self)
        self.focus_set()


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
                                   filename)
            self.tracks += track
            self.a_playlist_pane.append(track)
            self.a_playlist_pane.treeview.select(filename)
        self.a_playlist_pane.treeview.focus_set()


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
                if (form.edited_track is not None and
                        form.edited_track.title != track.title):
                    track.title = form.edited_track.title
                    self.tracks.save()
                    self.a_playlist_pane.update(iid, track)
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
            if self.playing is not None:
                self.on_play_or_pause_track() # Pause/Stop
            treeview.select(prev_iid)
            self.on_play_or_pause_track() # Play


    def on_play_or_pause_track(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            if self.playing is None:
                if iid == Player.player.filename:
                    Player.player.resume()
                else:
                    if not self.play_track(treeview, iid):
                        return
                icon = PAUSE_ICON
                self.playing = iid
                self.while_playing()
            else:
                Player.player.pause()
                icon = PLAY_ICON
                self.playing = None
                self.winfo_toplevel().title(f'{APPNAME} v{VERSION}')
            self.play_pause_button.config(image=self.images[icon])


    def play_track(self, treeview, iid):
        self.position_var.set(0)
        ok, err = Player.player.play(iid)
        if ok:
            length = Player.player.length
            self.position_progressbar.configure(maximum=length)
            track = self.tracks[treeview.index(iid)]
            length = round(length)
            if track.secs != length:
                track.secs = length
                self.tracks.save()
                self.a_playlist_pane.update(iid, track)
            self.update_volume()
            self.set_status_message(track.title, millisec=None)
            self.winfo_toplevel().title(f'{track.title} • {APPNAME}')
            self.track_data_timer_id = self.after(
                100, lambda _event=None: self.show_track_data(track.title))
        else:
            message = self.status_label.cget('text')
            self.set_status_message(err, fg=ERROR_FG)
            if message: # restore original message
                self.status_timer_id = self.after(
                    10_000, lambda: self.set_status_message(message,
                                                            millisec=None))
        return ok


    def on_next_track(self, _event=None):
        if self.tracks is None:
            return
        treeview = self.a_playlist_pane.treeview
        iid = treeview.focus()
        if iid:
            next_iid = treeview.next(iid)
            if not next_iid:
                return # Can't go after last one
            if self.playing is not None:
                self.on_play_or_pause_track() # Pause/Stop
            treeview.select(next_iid)
            self.on_play_or_pause_track() # Play


    def while_playing(self, _event=None):
        if self.playing_timer_id is not None:
            self.after_cancel(self.playing_timer_id)
            self.playing_timer_id = None
        if self.playing is not None:
            pos = Player.player.pos
            length = Player.player.length
            if math.isclose(pos, length):
                self.on_play_or_pause_track() # Pause/Stop
                self.on_next_track()
            else:
                self.set_progress(pos, length)
                self.position_var.set(pos)
                self.playing_timer_id = self.after(1000, self.while_playing)


    def maybe_update_times(self, name):
        if not Player.player.valid:
            return
        top = self.winfo_toplevel()
        try:
            top.config(cursor='watch')
            top.update_idletasks()
            self.volume_var.set(0.0)
            changed = 0
            for track in self.tracks:
                if track.secs <= 0:
                    changed += self.update_time(track)
            if changed:
                self.tracks.save()
                self.set_status_message(
                    f'{len(self.tracks):,} tracks in {name} of '
                    f'{self.tracks.humanized_length}', millisec=None)
        finally:
            top.config(cursor='arrow')
            self.volume_var.set(Config.config.current_volume or 0.5)


    def update_time(self, track):
        ok, _ = Player.player.play(track.filename)
        if ok:
            length = round(Player.player.length)
            Player.player.stop()
            if length > 0:
                track.secs = length
                self.a_playlist_pane.update(track.filename, track)
                return 1
        return 0


    def show_track_data(self, title):
        if self.track_data_timer_id is not None:
            self.after_cancel(self.track_data_timer_id)
            self.track_data_timer_id = None
        data = Player.player.track_data
        message = f'#{data.number} {data.album} • {data.artist}'
        if data.title != title:
            message = f'{data.title} {message}'
        self.set_status_message(message, millisec=None)
