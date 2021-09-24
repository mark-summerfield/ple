#!/usr/bin/env python3
# Copyright © 2021 Mark Summerfield. All rights reserved.
# License: GPLv3

import atexit
import collections
import pathlib
import threading

try: # 1..4 order must be preserved
    import gi  # 1
    gi.require_version('Gst', '1.0') # 2
    from gi.repository import Gst, GObject  # 3
    Gst.init() # 4
    _GST = True
except (ImportError, ValueError):
    _GST = False


TrackData = collections.namedtuple(
    'TrackData', 'title number album artist', defaults=('', 0, '', ''))


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
            self._volume = 0.5
            self._uri = None
            self._playbin = Gst.ElementFactory.make('playbin', None)
            self._bus = self._playbin.get_bus()
            self._bus.add_signal_watch()
            self._bus.connect('message', self.on_bus_call)
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
            self._volume = max(0.0, min(1.0, value))
            self._playbin.set_property('volume', self._volume)


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
            if status[0] == Gst.StateChangeReturn.FAILURE:
                word = 'play' if pathlib.Path(filename).exists() else 'find'
                return False, f'Failed to {word} {filename}'
            return True, None


        def pause(self):
            self._playbin.set_state(Gst.State.PAUSED)


        def resume(self):
            self._playbin.set_state(Gst.State.PLAYING)


        def stop(self):
            self._playbin.set_state(Gst.State.NULL)


        def on_bus_call(self, _bus, message):
            if message.type == Gst.MessageType.TAG:
                tags = message.parse_tag()
                d = {}
                for i in range(tags.n_tags()):
                    tag = tags.nth_tag_name(i)
                    value = tags.get_value_index(tag, 0)
                    if tag == 'track-number':
                        tag = 'number'
                    if tag in TrackData._fields:
                        d[tag] = value
                if d.get('title', ''):
                    data = TrackData(**d)
                    print(data) # TODO show in UI


        def close(self):
            self._uri = None
            self._playbin.set_state(Gst.State.NULL)


player = _Player()
atexit.register(player.close)
