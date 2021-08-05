#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
+----------------------------------------------------
|[Open...] [Config...] | [Add] [Edit] [Move Up] [Move Down] \
                         [Remove] [Save] [About] [Quit]
                         [<<] [>#] [>>]
+-----------------------------------------------------
| tree view showing    | list of titles (& times?) in
| folders +            | current (highlighted) playlist
| *.{m3u,pls,xspf}     | from left panel (if any)
|                      |
|         :            |             :
+-----------------------------------------------------

Open: open folder
Config: default music folder; default playlists folder
Add: add one or more new tracks to the current playlist
Edit: edit the title of the current track in the current playlist
Move Up: move the current track up one in the current playlist
Move Down: move the current track down one in the current playlist
Remove: remove the current track from the current playlist
Save: save the current playlist
Quit: offer save unsaved changes/quit/cancel if dirty then quit
<< Play Prev: only show if default player is PLE
># Play|Pause: if default player is external then only show [>] Play and
               when clicked send the current track to the player; if the
               track plays to the end automatically makes the next track
               current and starts playing it and so on until the end of the
               playlist
>> Play Next: only show if default player is PLE
About: show about box
'''

import datetime
import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import Const
import Tooltip


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=Const.PAD)
        self.images = {}
        self.make_images()
        self.make_widgets()
        self.make_layout()


    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (Const.FILEOPEN_ICON, Const.CONFIG_ICON):
            self.images[name] = tk.PhotoImage(file=path / name)


    def make_widgets(self):
        self.make_buttons()


    def make_buttons(self):
        self.toolbar = ttk.Frame(self.master)
        self.folder_open_button = ttk.Button(
            self.toolbar, image=self.images[Const.FILEOPEN_ICON],
            command=self.on_file_open)
        Tooltip.Tooltip(self.folder_open_button, 'Open Playlist Folder...')
        self.config_button = ttk.Button(
            self.toolbar, image=self.images[Const.CONFIG_ICON],
            command=self.on_config)
        Tooltip.Tooltip(self.config_button, 'Configure...')


    def make_layout(self):
        self.folder_open_button.grid(row=0, column=0, padx=Const.PAD,
                                     sticky=tk.W)
        self.config_button.grid(row=0, column=1, padx=Const.PAD,
                                sticky=tk.W)
        self.toolbar.grid(row=0, column=0, padx=Const.PAD, pady=Const.PAD,
                          sticky=tk.W + tk.E)
        self.master.winfo_toplevel().columnconfigure(0, weight=1)
        self.master.winfo_toplevel().rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


    def on_file_open(self, _event=None):
        print('on_file_open')


    def on_config(self, _event=None):
        print('on_config')


    def on_about(self, _event=None):
        year = datetime.date.today().year
        if year > 2020:
            year = f'2020-{year - 2000}'
        tk.messagebox.showinfo(f'{Const.APPNAME} — About', f'''\
{Const.APPNAME} v{Const.VERSION}

Copyright © {year} Mark Summerfield. All rights reserved.
License: GPLv3

An application for creating and modifying playlists and for playing \
tracks and playlists.''')


    def on_close(self):
        # TODO prompt to save unsaved changes
        print('on_close(): prompt to save unsaved changes')
        self.quit()
