#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import atexit
import threading

try: # 1..4 order must be preserved
    import gi  # 1
    gi.require_version('Gst', '1.0') # 2
    from gi.repository import Gst, GObject  # 3
    Gst.init() # 4
    _GST = True
except (ImportError, ValueError):
    _GST = False


if not _GST:
    class _Player:

        @property
        def valid(self):
            return False


        def close(self):
            pass
else:
    class _Player:

        _gloop_thread = None

        def __init__(self):
            self._volume = 50
            self._uri = None
            self._playbin = Gst.ElementFactory.make('playbin', None)
            if _Player._gloop_thread is None:
                _Player._gloop_thread = threading.Thread(
                    target=GObject.MainLoop().run)
                _Player._gloop_thread.daemon = True
                _Player._gloop_thread.start()


        @property
        def valid(self):
            return True


        @property
        def filename(self): # strip leading file://
            return self._uri[7:] if self._uri is not None else None


        @property
        def volume(self):
            return self._volume


        @volume.setter
        def volume(self, value):
            self._volume = max(0, min(100, value))
            self._set_volume()


        def _set_volume(self): # range 0.0..1.0
            self._playbin.set_property('volume', self._volume / 100.0)


        @property
        def pos(self):
            ok, time_pos = self._playbin.query_position(Gst.Format.TIME)
            return (time_pos / Gst.SECOND) if ok else 0


        @property
        def length(self):
            ok, duration = self._playbin.query_duration(Gst.Format.TIME)
            return (duration / Gst.SECOND) if ok else 0


        def play(self, filename):
            self._uri = (filename if filename.startswith('file://') else
                         f'file://{filename}')
            self._playbin.set_state(Gst.State.READY)
            self._playbin.set_property('uri', self._uri)
            self._playbin.set_state(Gst.State.PLAYING)
            status = self._playbin.get_state(Gst.CLOCK_TIME_NONE)
            return status[0] != Gst.StateChangeReturn.FAILURE


        def pause(self):
            self._playbin.set_state(Gst.State.PAUSED)


        def resume(self):
            self._playbin.set_state(Gst.State.PLAYING)


        def close(self):
            self._uri = None
            self._playbin.set_state(Gst.State.NULL)


player = _Player()
atexit.register(player.close)
