#!/bin/bash
tokei -f -tPython
unrecognized.py -q
python3 -m flake8 --ignore=W504,E261,E303 .
python3 -m vulture . \
    | grep -v Window.py.*unused.class.*60 \
    | grep -v .*Form.py.*unused.method..body \
    | grep -v .*Form.py.*unused.method..buttonbox \
    | grep -v .*Form.py.*unused.method..validate
git st
