#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import pathlib
import tkinter as tk
import tkinter.font as tkfont

import Config
import Window
from Const import APPNAME, VERSION


def main():
    app = tk.Tk()
    app.withdraw()
    app.minsize(640, 480)
    set_default_fonts(app)
    config = Config.config
    app.geometry(config.geometry)
    app.title(f'{APPNAME} v{VERSION}')
    app.option_add('*tearOff', False)
    app.option_add('*insertOffTime', config.cursor_blink_rate)
    imagepath = pathlib.Path(__file__).resolve().parent / 'images/'
    app.iconphoto(True, tk.PhotoImage(file=imagepath / 'ple.png'))
    window = Window.Window(app, imagepath)
    app.protocol('WM_DELETE_WINDOW', window.on_close)
    app.deiconify()
    app.mainloop()


def set_default_fonts(app):
    config = Config.config
    size = config.base_font_size
    for name in ('TkCaptionFont', 'TkDefaultFont', 'TkFixedFont',
                 'TkMenuFont', 'TkIconFont', 'TkTextFont'):
        tkfont.nametofont(name).configure(size=size)
    tkfont.nametofont('TkHeadingFont').configure(size=size,
                                                 weight=tk.NORMAL)
    size -= 1
    for name in ('TkSmallCaptionFont', 'TkTooltipFont',):
        tkfont.nametofont(name).configure(size=size)


if __name__ == '__main__':
    main()
