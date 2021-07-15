#!/bin/bash
tokei -f -tPython 
unrecognized.py -q
python3 -m flake8 .
python3 -m vulture .
git st
