#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscrolledtext
import tkinter.ttk as ttk

import Config
import Player
from Const import APPNAME, NSWE, PAD


class Form(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title(f'Help — {APPNAME}')
        self.geometry('640x480')
        self.make_widgets()
        self.make_layout()
        self.make_bindings()


    def make_widgets(self):
        self.box = ttk.Frame(self)
        self.text = tkscrolledtext.ScrolledText(self.box)
        self.make_tags()
        self.populate_text()
        self.text.config(state=tk.DISABLED) # read-only
        self.button = ttk.Button(self.box, text='OK', underline=0,
                                 command=self.quit)


    def make_layout(self):
        self.text.grid(row=0, column=0, sticky=NSWE, pady=PAD)
        self.button.grid(row=1, column=0, padx=PAD, pady=PAD)
        self.box.grid(row=0, column=0, sticky=NSWE)
        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid_rowconfigure(0, weight=1)
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


    def make_bindings(self):
        self.bind('<Return>', lambda *_: self.button.invoke())
        self.bind('<Alt-o>', lambda *_: self.button.invoke())
        self.bind('<Escape>', lambda *_: self.button.invoke())


    def make_tags(self):
        config = Config.config
        size = config.base_font_size
        default_font = tkfont.nametofont('TkDefaultFont')
        title_font = tkfont.Font(family=default_font.cget('family'),
                                 size=size + 2, weight='bold')
        self.text.tag_config('title', font=title_font, foreground='navy',
                             justify=tk.CENTER)
        table_title_font = default_font.copy()
        table_title_font.configure(underline=True)
        tab = '5.75c'
        margin = '1m'
        self.text.tag_config(
            'rowtitle', tabs=(tab,), font=table_title_font,
            foreground='darkgreen', lmargin1=margin)
        self.text.tag_config('row', tabs=(tab,), font=default_font,
                             lmargin1=margin)
        self.text.tag_config('key', foreground='blue')
        italic = default_font.copy()
        italic.configure(slant='italic')
        self.text.tag_config('italic', font=italic)
        self.text.tag_config('col1', lmargin1=tab, lmargin2=tab)


    def populate_text(self):
        def add(text, *tags):
            self.text.insert(tk.END, text, tags)

        add('PlayList Editor\n', 'title')
        add('Input\tAction\n', 'rowtitle')
        if Player.player.valid:
            add('Double-Click', 'row', 'key')
            add(' or\n', 'row', 'italic')
            add('    Enter', 'row', 'key')
            add(' or ', 'row', 'italic')
            add('Spacebar', 'row', 'key')
            add('\tPlay or pause the current track\n', 'row', 'col1')
        add('Alt+A', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+A', 'row', 'key')
        add('\tAdd a new track to the current playlist\n', 'row', 'col1')
        add('Alt+B', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+B', 'row', 'key')
        add('\tShow the about box\n', 'row', 'col1')
        add('Alt+D', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+D', 'row', 'key')
        add('\tMove the current track down\n', 'row', 'col1')
        add('Alt+E', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+E', 'row', 'key')
        add('\tEdit the current track\n', 'row', 'col1')
        add('F1', 'row', 'key')
        add(' or\n', 'row', 'italic')
        add('    Alt+H', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+H', 'row', 'key')
        add('\tShow this help window\n', 'row', 'col1')
        add('Alt+I', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+I', 'row', 'key')
        add('\tPop up the history menu\n', 'row', 'col1')
        add('Alt+M', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+M', 'row', 'key')
        add('\tUnremove the last removed track\n', 'row', 'col1')
        add('Alt+N', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+N', 'row', 'key')
        add('\tCreate a new playlist\n', 'row', 'col1')
        if Player.player.valid:
            add('Ctrl+P', 'row', 'key')
            add('\tPlay the previous track\n', 'row', 'col1')
        add('Alt+O', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+O', 'row', 'key')
        add(f"\tEdit {APPNAME}'s options\n", 'row', 'col1')
        add('Esccape', 'row', 'key')
        add(' or\n', 'row', 'italic')
        add('    Alt+Q', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+Q', 'row', 'key')
        add('\tQuit\n', 'row', 'col1')
        add('Alt+R', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+R', 'row', 'key')
        add('\tRemove the current track\n', 'row', 'col1')
        if Player.player.valid:
            add('Ctrl+T', 'row', 'key')
            add('\tPlay the next track\n', 'row', 'col1')
        add('Alt+U', 'row', 'key')
        add(' or ', 'row', 'italic')
        add('Ctrl+U', 'row', 'key')
        add('\tMove the current track up\n', 'row', 'col1')


    def quit(self, _event=None):
        self.destroy()
        self.master.focus_set()
