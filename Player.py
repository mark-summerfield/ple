#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3


class _Player:

    @property
    def valid(self): # TODO for testing return True
        return True # only return True if it can play audio


player = _Player()
