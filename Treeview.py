#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import tkinter as tk
import tkinter.ttk as ttk


class Treeview(ttk.Treeview):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        yscroller = ttk.Scrollbar(master, orient=tk.VERTICAL,
                                  command=self.yview)
        xscroller = ttk.Scrollbar(master, orient=tk.HORIZONTAL,
                                  command=self.xview)
        self.configure(yscroll=yscroller.set, xscroll=xscroller.set)
        yscroller.grid(row=0, column=1, sticky=tk.N + tk.S)
        xscroller.grid(row=1, column=0, sticky=tk.W + tk.E)


    def clear(self):
        self.delete(*self.get_children())
