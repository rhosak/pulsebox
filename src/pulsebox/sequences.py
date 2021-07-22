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
