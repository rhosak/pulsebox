#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sequences.py
Handling of sequence specifications for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

from copy import deepcopy
from operator import attrgetter

import pulsebox.codeblocks as pcb
import pulsebox.events as pev
from pulsebox.config import pulsebox_pincount


class FlipSequence():
    def __init__(self, flips = []):
        self.flips = flips

    def sort_flips(self):
        self.flips.sort(key=attrgetter("timestamp"))


class Sequence():
    def __init__(self, events = [], triggered=False, parameter=1000):
        self.events = events
        self.loop_counter = 0
        self.time = 0
        self.triggered = triggered
        self.parameter = parameter

    def code(self):
        code = "\n".join([pcb.header(), pcb.setup(), ""])
        if not self.events:
            code += "   ;\n"
        else:
            code += "\n".join([event.codeblock for event in self.events] + [""])
        code += pcb.end()
        return code

    @classmethod
    def from_flip_sequence(cls, fs, triggered=False, parameter=1000):
        events = []  # We will store the low-level events here
        time = 0  # keep track of 'current' time as we go through the flips
        loop_counter = 0
        channel_states = [0] * pulsebox_pincount  # Every channels starts at 0.

        if not fs.flips:
            return cls(events)

        # This technique relies on using `pop()`, which eliminates the last
        # element of an array. So (1) we copy the array of flip events and
        # (2) we are going to reverse it, so `pop()` effectively eliminates
        # the first (smallest-timestamp) element.
        flips = deepcopy(fs.flips)
        flips.sort(key=attrgetter("timestamp"), reverse=True)

        # Go through all of the flips and create low level
        # `DelayEvent` and `StateChangeEvent` instances as needed.
        flip = flips.pop()
        out_of_flips = False
        while True:
            # Check the timestamp of the flip. Do we need a delay?
            required_delay = flip.timestamp - time
            required_iters = pev.time2iters(required_delay)
            if required_iters > 0:
                events.append(pev.DelayEvent(iters=required_iters,
                                             loop_suffix=str(loop_counter)))
                loop_counter += 1
            time += required_delay  # advance time

            # Change the channel state for all channels where a flip
            # is occuring right at this time.
            # Also check that we are not going to flip the same channel
            # more than once. Raise an error if that is the case.
            flipped_channels = []
            while flip.timestamp == time:
                if flip.channel in flipped_channels:
                    raise ValueError("Multiple flips of the same channel " \
                                     "occuring at the same time are forbidden.")
                channel_states[flip.channel] += 1
                channel_states[flip.channel] %= 2
                flipped_channels.append(flip.channel)
                if flips:
                    flip = flips.pop()
                else:
                    out_of_flips = True
                    break

            # Funny thing: If you create a StateChangeEvent with given
            # channel_states and then change this variable later on, the
            # event changes as well. Using deepcopy to prevent this.
            events.append(pev.StateChangeEvent(deepcopy(channel_states)))

            if out_of_flips:
                break
        
        new_sequence = cls(events, triggered=triggered, parameter=parameter)
        new_sequence.time = time
        new_sequence.loop_counter = loop_counter

        return new_sequence

    def __repr__(self):
        msg = f"Sequence - duration: {self.time} s, loops: {self.loop_counter}\n"
        msg += "\t* " + str(self.events[:10]).strip("[]").replace(", ",
                                                                  "\n\t* ")
        if len(self.events) > 10:
            msg += "\n\t* ..."
        return msg
