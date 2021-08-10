#!/bin/bash
tokei -f -tPython -e audioplayerGUI.py -e playbin-example-audio.py
unrecognized.py -q
python3 -m flake8 --ignore=W504,E261,E303 . \
    | grep -v audioplayerGUI.py \
    | grep -v playbin-example-audio.py
python3 -m vulture . \
    | grep -v audioplayerGUI.py \
    | grep -v playbin-example-audio.py \
    | grep -v AboutForm.*unused.method..body \
    | grep -v AboutForm.*unused.method..buttonbox
git st
