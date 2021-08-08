#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3
#
# This module is a simplification and adaptation of the code provided by
# Michael Lange at http://tkinter.unpy.net/wiki/ToolTip

'''
Usage: ToolTip.Tooltip(widget, text='Tool tip text')
'''

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk


class Tooltip:

    delay = 600
    show_time = 5_000
    background = 'lightyellow'

    def __init__(self, master, text):
        self.master = master
        self.text = text
        self.timer_id = None
        self.tip = None
        self.master.bind('<Enter>', self.enter, '+')
        self.master.bind('<Leave>', self.leave, '+')


    def enter(self, _event=None):
        if self.timer_id is None and self.tip is None:
            self.timer_id = self.master.after(Tooltip.delay, self.show)


    def leave(self, _event=None):
        if self.timer_id is not None:
            id = self.timer_id
            self.timer_id = None
            self.master.after_cancel(id)
        self.hide()


    def hide(self):
        if self.tip is not None:
            tip = self.tip
            self.tip = None
            tip.destroy()


    def show(self):
        self.leave()
        self.tip = tk.Toplevel(self.master)
        self.tip.withdraw() # Don't show until we have the geometry
        self.tip.wm_overrideredirect(True) # No window decorations etc.
        label = ttk.Label(
            self.tip, text=self.text, padding=1,
            background=Tooltip.background, wraplength=480,
            relief=tk.GROOVE, font=tkfont.nametofont('TkTooltipFont'))
        label.pack()
        x, y = self.position()
        self.tip.wm_geometry('+{}+{}'.format(x, y))
        self.tip.deiconify()
        if self.master.winfo_viewable():
            self.tip.transient(self.master)
        self.tip.update_idletasks()
        self.timer_id = self.master.after(Tooltip.show_time, self.hide)


    def position(self):
        tipx = self.tip.winfo_reqwidth()
        tipy = self.tip.winfo_reqheight()
        width = self.tip.winfo_screenwidth()
        height = self.tip.winfo_screenheight()
        y = self.master.winfo_rooty() + self.master.winfo_height()
        if y + tipy > height:
            y = self.master.winfo_rooty() - tipy
        x = self.tip.winfo_pointerx()
        if x < 0:
            x = 0
        elif x + tipx > width:
            x = width - tipx
        return x, y
