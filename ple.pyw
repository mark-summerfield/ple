#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import os
import tkinter as tk
import tkinter.font as tkfont

import Config
import Const
import Window


def main():
    app = tk.Tk()
    app.withdraw()
    app.minsize(320, 240)
    config = Config.config
    size = config.base_font_size
    tkfont.nametofont('TkDefaultFont').configure(size=size)
    tkfont.nametofont('TkHeadingFont').configure(size=size,
                                                 weight=tk.NORMAL)
    tkfont.nametofont('TkTooltipFont').configure(size=size - 1)
    app.geometry(config.geometry)
    app.title(f'{Const.APPNAME} v{Const.VERSION}')
    app.option_add('*tearOff', False)
    app.option_add('*insertOffTime', 0) # Should be user customizable
    icon = os.path.join(os.path.dirname(__file__), 'images/ple.png')
    app.iconphoto(True, tk.PhotoImage(file=icon))
    window = Window.Window(app)
    app.protocol('WM_DELETE_WINDOW', window.on_close)
    app.deiconify()
    app.mainloop()


if __name__ == '__main__':
    main()
