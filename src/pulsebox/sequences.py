#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sequences.py
Handling of sequence specifications for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

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
    number, unit = time_string[:-1], time_string[-1]
    try:
        factor = factors[unit]
    except KeyError:
        raise ValueError("Invalid time unit given.")
    time = number * factor
    return time
