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
from Const import APPNAME, PAD, VERSION


class Form(tkdialog.Dialog):

    def __init__(self, master):
        super().__init__(master, f'About — {APPNAME}')


    def body(self, master):
        year = datetime.date.today().year
        if year > 2021:
            year = f'2021-{year - 2000}'
        self.icon = tk.PhotoImage(
            file=(pathlib.Path(__file__).parent / 'images/ple.png'))
        imageLabel = ttk.Label(master, image=self.icon, anchor=tk.CENTER)
        std_font = tkfont.nametofont('TkDefaultFont')
        font = tkfont.Font(family=std_font.cget('family'),
                           size=int(std_font.cget('size')) + 1,
                           weight=tkfont.BOLD)
        captionLabel = ttk.Label(
            master, foreground='navy', anchor=tk.CENTER, justify=tk.CENTER,
            text=f'{APPNAME} v{VERSION}', font=font)
        desc = 'An application for creating and editing playlists'
        desc += ('\nand for playing tracks and entire playlists.'
                 if Player.player.valid else '.')
        bodyLabel = ttk.Label(master, anchor=tk.CENTER, justify=tk.CENTER,
                              text=f'''
Copyright © {year} Mark Summerfield. All Rights Reserved.
License: GPLv3

{desc}
________________________________________

Python \
{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
Tk {tk.TkVersion}
{platform.platform()}
''')
        imageLabel.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S,
                        pady=PAD * 2)
        captionLabel.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E,
                          pady=PAD)
        bodyLabel.grid(row=2, column=0, sticky=tk.W + tk.E + tk.N + tk.S,
                       pady=PAD)


    def buttonbox(self):
        self.ok_icon = tk.PhotoImage(
            file=(pathlib.Path(__file__).parent / 'images/dialog-ok.png'))
        box = ttk.Frame(self)
        okButton = ttk.Button(box, text='OK', underline=0, command=self.ok,
                              image=self.ok_icon, compound=tk.LEFT)
        okButton.pack(pady=3)
        box.pack()
        self.bind('<Return>', self.ok)
        self.bind('<Alt-o>', self.ok)
        self.bind('<Escape>', self.cancel)
