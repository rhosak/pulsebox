#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""events.py
Pulse sequence events for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

from functools import reduce

from pulsebox.codeblocks import state_change, loop, channel_states_to_odsr
from pulsebox.config import calibration, pulsebox_pincount


class DelayEvent():
    def __init__(self, time_string=None, iters=None,
                 duration=None, loop_suffix="0"):
        if time_string:
            duration = read_time(time_string)
            iters = time2iters(duration)
        elif duration:
            iters = time2iters(duration)
        elif iters:
            duration = calibration * iters

        codeblock = loop(iters, loop_suffix)

        self.duration = duration
        self.iters = iters
        self.loop_suffix = loop_suffix
        self.codeblock = codeblock

    def from_time_string(self):
        duration = read_time(time_string)
        __init__(self, duration)

    def __repr__(self):
        return f"Delay: {self.duration} s " \
               f"({self.iters} iters)"


class StateChangeEvent():
    def __init__(self, channel_states):
        odsr = channel_states_to_odsr(channel_states)
        codeblock = state_change(odsr_value=odsr)
        
        self.channel_states = channel_states
        self.odsr = odsr
        self.codeblock = codeblock

    def __repr__(self):
        # msg = "Pulsebox state change: \n"
        msg = "State change: "
        for channel, state in enumerate(self.channel_states):
            msg += f"{state}"
            if channel % 4 == 3 and (channel + 1) < pulsebox_pincount:
                msg +="."
            # msg += f"\tCH{channel}: {state}"
        msg += f" ({self.odsr})"
        return msg


class PulseEvent():
    def __init__(self, channel, timestamp, duration):
        self.channel = channel
        self.timestamp = timestamp
        self.duration = duration
        self.flips = [FlipEvent(channel, timestamp=timestamp),
                      FlipEvent(channel, timestamp=(timestamp+duration))]

    def __repr__(self):
        return f"Pulse on channel {self.channel} - " \
               f"start: {self.timestamp} s, duration: {self.duration} s"

class FlipEvent():
    """The fundamental channel flip event.
    User pulse sequence input is transformed into a sequence
    of pulsebox channel flips.
    """
    def __init__(self, channel, time_string=None, timestamp=None):
        if not timestamp:
            if not time_string:
                raise ValueError("Neither time string nor timestamp given.")
            timestamp = read_time(time_string)
        self.channel = channel
        self.timestamp = timestamp

    def __repr__(self):
        return f"Channel {self.channel} flip at {self.timestamp} s"

def read_time(time_string):
    """Calculate time from a string containing a number and a time unit.
    
    The unit is denoted by the last character of `time_string`. Time is
    calculated by multiplying the 'number part' of `time_string` by a factor
    corresponding to the unit.
    
    The following units are accepted:

        * n: nanoseconds (factor = 1e-9)
        * u: microseconds (1e-6)
        * m: milliseconds (1e-3)
        * s: seconds (1)
        * TODO: c: MCU clock cycles (12e-9)
        * TODO: i: delay loop iterations (see `calibration` in config.ini)
    
    Args:
        * time_string (str): The (number + unit) string, for example "1m"
    
    Returns:
        * float time: Time (in seconds).
    """
    factors = {
        "n": 1e-9,
        "u": 1e-6,
        "m": 1e-3,
        "s": 1
    }
    
    # Check that the time string is properly formatted, e. g. time part
    # is followed by the unit part. The string should contain at least two
    # character, otherwise splitting it into two parts will raise an IndexError.
    try:
        number, unit = time_string[:-1], time_string[-1]
    except (IndexError, TypeError):
        raise ValueError("Invalid time string given.")

    # If the 'time part' cannot be converted to float, this raises a ValueError.
    number = float(number)
    
    if number < 0:
        raise ValueError("Negative time values are not allowed.")
    
    # Check that a valid time unit was specified. If no unit was specified,
    # then what we call 'unit' will in fact be the last digit of the time value
    # and as we do not use numeric unit symbols, we still get an error.
    try:
        factor = factors[unit]
    except KeyError:
        raise ValueError("Invalid time unit given.")

    time = number * factor
    return time

def time2iters(time):
    """Get the number of loop iterations required to achieve a given time delay.
    
    Args:
        * time (float): The time to convert to the number of delay loop iters.

    Returns:
        * int iters: The number of iterations through the ASM delay loop
            required to produce a delay of a given length.

    Notes:
        The possible delay times are discrete, with a step given by the
        structure of the ASM loop. This step is given by the `calibration`
        variable in the config.
        
        For example, if our delays for 1, 2, and 3 delay loop iterations are
        50 ns, 100 ns, and 150 ns, respectively, and we want to convert
        120 ns to delay loop iterations, we would see that 2.4 iterations are
        required. As this is impossible, we round this to the nearest integer
        amount of iterations. In this case, that's 2 iterations and instead of
        120 ns delay we produced a 100 ns delay.
    """
    if time < 0:
        raise ValueError("Negative time is not allowed.")
    iters = int(round(time / calibration))
    return iters


def parse_events(event_string, channel=None):
    """Convert a long string of events into an array of event instances.
    """
    event_substrings = event_string.split(" ")
    events = []
    for substring in event_substrings:
        try:
            event_type, event_params = substring[0], substring[1:]
        except (IndexError, ValueError):
            print(f"CH {channel} - Invalid event string: " \
                  f"{event_string.__repr__()}")
            return events
        if event_type.lower() == "p":  # PulseEvent
            # Pulse event contains two timestrings - start and duration.
            # Separate them.
            timestamp, duration = None, None
            for n, ch in enumerate(event_params):
                if ch.isalpha():
                    timestamp = read_time(event_params[:n+1])
                    duration = read_time(event_params[n+1:])
                    break
            pe = PulseEvent(channel, timestamp, duration)
            new_events = pe.flips
        for event in new_events:
            events.append(event)
    return events
