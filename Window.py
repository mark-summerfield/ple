#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

# TODO for folder_view show only the playlist name + a folder|file icon
# TODO auto-open the top-level folder at startup

'''
+----------------------------------------------------
|[New...][Open...] [Config...] | [Add] [Edit] [Move Up] [Move Down] \
                         [Remove] [Save] [About] [Quit]
                         [<<] [>#] [>>]
+-----------------------------------------------------
| tree view showing    | list of titles (& times?) in
| folders +            | current (highlighted) playlist
| *.{m3u,pls,xspf}     | from left panel (if any)
|                      |
|         :            |             :
+-----------------------------------------------------

New: create new empty playlist
Open: open folder
Config: default music folder; default playlists folder
Add: add one or more new tracks to the current playlist
Edit: edit the title of the current track in the current playlist
Move Up: move the current track up one in the current playlist
Move Down: move the current track down one in the current playlist
Remove: remove the current track from the current playlist
Save: save the current playlist (Save As, if 'Unnamed')
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
import glob
import os
import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import Config
import Const
import Tooltip


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=Const.PAD)
        self.images = {}
        self.make_images()
        self.make_widgets()
        self.make_layout()
        self.make_bindings()
        os.chdir(Config.config.playlists_path)
        self.folder_populate_roots()


    def make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (Const.FILEOPEN_ICON, Const.CONFIG_ICON,
                     Const.FILENEW_ICON,):
            self.images[name] = tk.PhotoImage(file=path / name)


    def make_widgets(self):
        self.make_buttons()
        self.make_folder_view()
        self.make_playlist_view()


    def make_buttons(self):
        self.button_frame = ttk.Frame(self.master)
        self.file_new_button = ttk.Button(
            self.button_frame, text='New…', underline=0,
            image=self.images[Const.FILENEW_ICON],
            command=self.on_file_new, compound=tk.TOP)
        Tooltip.Tooltip(self.file_new_button, 'Create New Playlist… Ctrl+N')
        self.folder_open_button = ttk.Button(
            self.button_frame, text='Open…', underline=0,
            image=self.images[Const.FILEOPEN_ICON],
            command=self.on_file_open, compound=tk.TOP)
        Tooltip.Tooltip(self.folder_open_button,
                        'Open Playlist Folder… Ctrl+O')
        self.config_button = ttk.Button(
            self.button_frame, text='Options…',
            image=self.images[Const.CONFIG_ICON],
            command=self.on_config, compound=tk.TOP)
        Tooltip.Tooltip(self.config_button, f'Configure {Const.APPNAME}…')


    def make_folder_view(self):
        self.folder_frame = ttk.Frame(self.master)
        self.folder_view = ttk.Treeview(self.folder_frame,
                                        columns=('fullpath', 'kind'))
        yscroller = ttk.Scrollbar(self.folder_frame, orient=tk.VERTICAL,
                                  command=self.folder_view.yview)
        xscroller = ttk.Scrollbar(self.folder_frame, orient=tk.HORIZONTAL,
                                  command=self.folder_view.xview)
        self.folder_view.configure(yscroll=yscroller.set,
                                   xscroll=xscroller.set)
        self.folder_view.heading('#0', text='Playlists', anchor=tk.W)
        self.folder_view.grid(row=0, column=0,
                              sticky=tk.W + tk.E + tk.N + tk.S)
        yscroller.grid(row=0, column=1, sticky=tk.N + tk.S)
        xscroller.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.folder_frame.grid_columnconfigure(0, weight=1)
        self.folder_frame.grid_rowconfigure(0, weight=1)


    def make_playlist_view(self):
        self.playlist_frame = ttk.Frame(self.master)
        self.playlist_view = ttk.Treeview(self.playlist_frame)
        yscroller = ttk.Scrollbar(self.playlist_frame, orient=tk.VERTICAL,
                                  command=self.playlist_view.yview)
        xscroller = ttk.Scrollbar(self.playlist_frame, orient=tk.HORIZONTAL,
                                  command=self.playlist_view.xview)
        self.playlist_view.configure(yscroll=yscroller.set,
                                     xscroll=xscroller.set)
        self.playlist_view.heading('#0', text='Playlist', anchor=tk.W)
        self.playlist_view.grid(row=0, column=0,
                                sticky=tk.W + tk.E + tk.N + tk.S)
        yscroller.grid(row=0, column=1, sticky=tk.N + tk.S)
        xscroller.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.playlist_frame.grid_columnconfigure(0, weight=1)
        self.playlist_frame.grid_rowconfigure(0, weight=1)


    def make_layout(self):
        self.file_new_button.grid(row=0, column=0, padx=Const.PAD,
                                  sticky=tk.W)
        self.folder_open_button.grid(row=0, column=1, padx=Const.PAD,
                                     sticky=tk.W)
        self.config_button.grid(row=0, column=2, padx=Const.PAD,
                                sticky=tk.W)
        self.button_frame.grid(row=0, column=0, padx=Const.PAD,
                               pady=Const.PAD, sticky=tk.W + tk.E,
                               columnspan=2)
        self.folder_frame.grid(row=1, column=0, padx=Const.PAD,
                               pady=Const.PAD,
                               sticky=tk.W + tk.E + tk.N + tk.S)
        self.playlist_frame.grid(row=1, column=1, padx=Const.PAD,
                                 pady=Const.PAD,
                                 sticky=tk.W + tk.E + tk.N + tk.S)
        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)


    def make_bindings(self):
        self.master.bind('<F5>', self.folder_update_tree)
        self.master.bind('<Alt-n>', self.on_file_new)
        self.master.bind('<Control-n>', self.on_file_new)
        self.master.bind('<Alt-o>', self.on_file_open)
        self.master.bind('<Control-o>', self.on_file_open)
        # self.master.bind('<Alt-s>', self.on_save)
        # self.master.bind('<Control-s>', self.on_save)
        self.master.bind('<Alt-q>', self.on_close)
        self.master.bind('<Control-q>', self.on_close)
        self.master.bind('<Escape>', self.on_close)
        self.folder_view.bind('<<TreeviewOpen>>', self.folder_update_tree)
        self.folder_view.bind('<Double-Button-1>', self.folder_change)




    def on_file_new(self, _event=None):
        print('on_file_new')


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


    def on_close(self, _event=None):
        # TODO prompt to save unsaved changes
        print('on_close(): prompt to save unsaved changes')
        self.quit()


    def folder_populate_roots(self):
        path = os.path.abspath('.')
        node = self.folder_view.insert('', tk.END, text=path,
                                       values=[path, 'folder'])
        self.folder_populate_tree(node)


    def folder_populate_tree(self, node):
        if self.folder_view.set(node, 'kind') != 'folder':
            return
        path = self.folder_view.set(node, 'fullpath')
        self.folder_view.delete(*self.folder_view.get_children(node))
        parent = self.folder_view.parent(node)
        special_dirs = [] if parent else glob.glob('.') + glob.glob('..')
        for name in special_dirs + os.listdir(path):
            kind = None
            name = os.path.join(path, name).replace('\\', '/')
            if os.path.isdir(name):
                kind = 'folder'
            elif os.path.isfile(name):
                kind = 'file'
            fname = os.path.split(name)[1]
            nid = self.folder_view.insert(node, tk.END, text=fname,
                                          values=[name, kind])
            if kind == 'folder':
                if fname not in {'.', '..'}:
                    self.folder_view.insert(nid, 0, text='dummy')
                    self.folder_view.item(nid, text=fname)


    def folder_update_tree(self, _event=None):
        self.folder_populate_tree(self.folder_view.focus())


    def folder_change(self, _event=None):
        node = self.folder_view.focus()
        if self.folder_view.parent(node):
            path = os.path.abspath(self.folder_view.set(node, 'fullpath'))
            if os.path.isdir(path):
                os.chdir(path)
                self.folder_view.delete(self.folder_view.get_children(''))
                self.folder_populate_roots()
