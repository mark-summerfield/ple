#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import datetime
import pathlib
import platform
import sys
import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as tkdialog
import tkinter.ttk as ttk

import Player
from Const import APPNAME, NSWE, PAD, PAD3, VERSION, WE


class Form(tkdialog.Dialog):

    def __init__(self, master):
        super().__init__(master, f'About — {APPNAME}')


    def body(self, master):
        self.make_body_widgets(master)
        self.make_body_layout(master)


    def make_body_widgets(self, master):
        year = datetime.date.today().year
        if year > 2021:
            year = f'2021-{year - 2000}'
        self.icon = tk.PhotoImage(
            file=(pathlib.Path(__file__).parent / 'images/ple.png'))
        self.image_label = ttk.Label(master, image=self.icon,
                                     anchor=tk.CENTER)
        std_font = tkfont.nametofont('TkDefaultFont')
        font = tkfont.Font(family=std_font.cget('family'),
                           size=int(std_font.cget('size')) + 1,
                           weight=tkfont.BOLD)
        self.caption_label = ttk.Label(
            master, foreground='navy', anchor=tk.CENTER, justify=tk.CENTER,
            text=f'{APPNAME} v{VERSION}', font=font)
        desc = 'An application for creating and editing playlists'
        desc += ('\nand for playing tracks and entire playlists.'
                 if Player.player.valid else '.')
        self.body_label = ttk.Label(master, anchor=tk.CENTER,
                                    justify=tk.CENTER, text=f'''
Copyright © {year} Mark Summerfield. All Rights Reserved.
License: GPLv3

{desc}
________________________________________

Python \
{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
Tk {tk.TkVersion}
{platform.platform()}''')


    def make_body_layout(self, master):
        self.image_label.grid(row=0, column=0, sticky=NSWE, pady=PAD)
        self.caption_label.grid(row=1, column=0, columnspan=2, sticky=WE,
                                pady=PAD)
        self.body_label.grid(row=2, column=0, sticky=NSWE)


    def buttonbox(self):
        self.make_buttons()
        self.make_button_layout()
        self.make_button_bindings()


    def make_buttons(self):
        self.ok_icon = tk.PhotoImage(
            file=(pathlib.Path(__file__).parent / 'images/dialog-ok.png'))
        self.box = ttk.Frame(self)
        self.ok_button = ttk.Button(
            self.box, text='OK', underline=0, command=self.ok,
            image=self.ok_icon, compound=tk.LEFT)


    def make_button_layout(self):
        self.ok_button.pack()
        self.box.pack(pady=PAD3)


    def make_button_bindings(self):
        self.bind('<Return>', lambda *_: self.ok_button.invoke())
        self.bind('<Alt-o>', lambda *_: self.ok_button.invoke())
        self.bind('<Escape>', self.cancel)
