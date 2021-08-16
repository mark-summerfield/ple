#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

from Const import APPNAME


class Form(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title(f'Help — {APPNAME}')
        self.geometry('640x480')
        # TODO
        self.make_bindings()


    def quit(self, _event=None):
        self.destroy()


    def make_bindings(self):
        self.bind('<Return>', self.quit)
        self.bind('<Alt-o>', self.quit)
        self.bind('<Escape>', self.quit)
