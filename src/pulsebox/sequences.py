#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sequences.py
Handling of sequence specifications for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

from copy import deepcopy
from operator import attrgetter

import pulsebox.events as pev
from pulsebox.config import pulsebox_pincount


class FlipSequence():
    def __init__(self, flips = []):
        self.flips = flips

    def sort_flips(self):
        self.flips.sort(key=attrgetter("timestamp"))


class Sequence():
    def __init__(self, events = [], init_states = [0] * pulsebox_pincount):
        self.events = events
        self.channel_states = init_states
        self.loop_counter = 0
        self.time = 0

    def from_flip_sequence(self, fs, init_states = [0] * pulsebox_pincount):
        fs.sort_flips()
        
        # This technique relies on using `pop()`, which eliminates the last
        # element of an array. So (1) we copy the array of flip events and
        # (2) we are going to reverse it, so `pop()` effectively eliminates
        # the first (smallest-timestamp) element.
        flips = deepcopy(fs.flips)[::-1]

        events = []  # We will store the low-level events here
        time = 0  # keep track of 'current' time as we go through the flips
        
        # Go through all of the flips and create low level
        # `DelayEvent` and `StateChangeEvent` instances as needed.
        while flips:
            # Check the timestamp of the flip. Do we need a delay?
            required_delay = flip.timestamp - time
            required_iters = pev.time2iters(required_delay)
            if required_iters > 0:
                events.append(pev.DelayEvent(iters=required_iters))
            time += required_delay
            
            # How many channel flips are happenning at once?
            
        __init__(self, events, init_states)
