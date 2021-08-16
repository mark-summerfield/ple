#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscrolledtext
import tkinter.ttk as ttk

import Config
from Const import APPNAME, NSWE, PAD, WE


class Form(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title(f'Help — {APPNAME}')
        self.geometry('640x480')
        # TODO
        config = Config.config
        size = config.base_font_size
        default_font = tkfont.nametofont('TkDefaultFont')
        title_font = tkfont.Font(family=default_font.cget('family'),
                                 size=size + 2, underline=True)
        text = tkscrolledtext.ScrolledText(self)
        text.tag_config('title', font=title_font, foreground='navy',
                        justify=tk.CENTER)
        table_title_font = default_font.copy()
        table_title_font.configure(underline=True)
        text.tag_config('row', tabs=('4c',), font=table_title_font,
                        foreground='darkgreen')
        text.insert(tk.END, 'Help\n', ('title',))
        text.insert(tk.END, 'Shortcut\tAction\n', ('row',))
        text.config(state=tk.DISABLED)
        text.grid(row=0, column=0, sticky=NSWE)
        ttk.Button(self, text='OK', underline=0, command=self.quit).grid(
                   row=1, column=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.bind('<Return>', self.quit)
        self.bind('<Alt-o>', self.quit)
        self.bind('<Escape>', self.quit)


    def quit(self, _event=None):
        self.destroy()
