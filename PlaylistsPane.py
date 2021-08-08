#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import os
import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import playlist


class PlaylistsPane(ttk.Frame):

    def __init__(self, master, *, padding, path):
        super().__init__(master, padding=padding)
        self.images = {}
        self._make_images()
        self.treeview = ttk.Treeview(self, selectmode=tk.BROWSE)
        yscroller = ttk.Scrollbar(self, orient=tk.VERTICAL,
                                  command=self.treeview.yview)
        xscroller = ttk.Scrollbar(self, orient=tk.HORIZONTAL,
                                  command=self.treeview.xview)
        self.treeview.configure(yscroll=yscroller.set,
                                xscroll=xscroller.set)
        self.treeview.grid(row=0, column=0,
                           sticky=tk.W + tk.E + tk.N + tk.S)
        yscroller.grid(row=0, column=1, sticky=tk.N + tk.S)
        xscroller.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.treeview.heading('#0', text='Playlists', anchor=tk.W)
        self.set_path(path)


    def set_focus(self):
        self.treeview.focus_set()
        tops = self.treeview.get_children()
        if tops:
            focus = tops[0]
            children = self.treeview.get_children(focus)
            if children:
                focus = children[0]
            self.treeview.focus(focus)
            self.treeview.selection_set(focus)


    def _make_images(self):
        path = pathlib.Path(__file__).parent / 'images'
        for name in (FOLDER_ICON, PLAYLIST_ICON, FOLDER_HOME_ICON):
            self.images[name] = tk.PhotoImage(file=path / name)


    def set_path(self, path):
        self.treeview.delete(*self.treeview.get_children())
        self.treeview.insert('', tk.END, path, text=path, open=True,
                             image=self.images[FOLDER_HOME_ICON])
        self._populate_tree(path)


    def _populate_tree(self, root):
        if not os.path.isdir(root):
            return
        folders = []
        files = []
        with os.scandir(root) as entries:
            for entry in entries:
                if not entry.name.startswith('.'):
                    if entry.is_dir():
                        folders.append((entry.path, entry.name))
                    elif playlist.is_playlist(entry.name):
                        files.append((entry.path, entry.name))

        def by_entry(entry):
            return entry[0].upper()

        for path, name in sorted(folders, key=by_entry):
            self.treeview.insert(root, tk.END, path, text=name,
                                 image=self.images[FOLDER_ICON])
            self._populate_tree(path)
        for path, name in sorted(files, key=by_entry):
            self.treeview.insert(root, tk.END, path, text=name,
                                 image=self.images[PLAYLIST_ICON])


FOLDER_HOME_ICON = 'folder_home.png'
FOLDER_ICON = 'folder.png'
PLAYLIST_ICON = 'playlist.png'


if __name__ == '__main__':
    app = tk.Tk()
    app.title('PlaylistsPane')
    app.minsize(400, 600)
    pane = PlaylistsPane(app, padding='0.75m',
                         path='/home/mark/data/playlists')
    pane.grid(sticky=tk.W + tk.E + tk.S + tk.N)
    pane.set_focus()
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    app.mainloop()
