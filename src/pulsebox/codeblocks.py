#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""codeblocks.py
Contains code blocks for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

import config

from functools import reduce

def header(msg=config.header):
    """A (usually) one-line comment written at the top of the .ino file.
    
    Kwargs:
        * msg (str): The message contained in the header.
            Default: See `header` in config.ini.
    
    Returns:
        * str hdr: The header (contents of `msg` wrapped in a comment).
        	If empty string `""` is given as input, return `None`.
    """
    if msg == "":
    	return None
    # We do not allow comment ending sequence "*/" to be present in `msg`.
    sanitized_msg = msg.replace("*/", "")
    hdr = f"/* {sanitized_msg} */"
    return hdr

def setup(triggered=False, parameter=None):
    """The beginning (setup part) of the .ino file.
    
    Kwargs:
        * triggered (bool): Run in triggered mode.
            If `False`, run in continuous (repeat) mode.
            Default: False
        * parameter (int): A parameter which depends on the chosen mode.
            Default value of `None` results in appropriate default value.
            - Triggered mode: trigger pin
                (the Arduino Due pin to which we attach an interrupt)
                Default: See `trigger_pin` in config.ini.
            - Continuous mode: delay between sequence repetitions (in ms).
                (uses the Arduino `delay()` function)
                Default: See `cont_mode_delay_ms` in config.ini.
    
    Returns:
        * str stp: The setup part of the .ino code.
    
    Notes:
        * For continuous (repeat) mode, the values of `parameter` (delay)
            can be of type float as long as they really represent an integer.
            An example of this would be 4.0 or 1e2.
        * The Arduino `delay()` function accepts a 32-bit unsigned int, so
            
    """
    stp = "void setup() {\n" \
          "   for (int i=1; i<=78; i++)\n" \
          "      detachInterrupt(i);\n" \
          "   void __disable_irq(void);\n" \
          f"   REG_PIOC_OER = {config.all_pins_enabled};\n" \
          f"   REG_PIOC_OWER = {config.all_pins_enabled};\n"
          
    # Triggered mode
    if triggered:
        trigger_pin = parameter if parameter else config.trigger_pin
        
        # Check that delay is an integer and a valid Arduino Due pin.
        # Also check that it is not identical to a defined pulsebox pin.
        if type(trigger_pin) is not int:
            raise TypeError("Trigger pin is not an int.")
        if not (0 <= trigger_pin <= 78):
            raise ValueError("Trigger pin is not a valid Arduino Due pin.")
        if trigger_pin in config.pulsebox_pins:
            raise ValueError("Trigger pin is identical to a pulsebox pin.")
        
        stp += f"   attachInterrupt({trigger_pin}, sequence, RISING);\n"
        
    # Continuous (repeat) mode
    else:
        delay = parameter if parameter else config.cont_mode_delay_ms
        
        # Check if `delay` is int. If not, attempt conversion (if safe).
        if type(delay) is not int:
            try:
                assert int(delay) == delay
                delay = int(delay)
            except (ValueError, AssertionError):
                raise TypeError("Continuous mode delay (ms) is not an int.")
        
        # Check that `delay` is a valid 32-bit unsigned int.
        if not 0 <= delay < 2**32:
            raise ValueError("Continuous mode delay (ms) is not a 32-bit int.")

        stp += "   while(1) {\n" \
               "      sequence();\n" \
               f"      delay({delay});\n" \
               "   }\n"

    stp += "}\n\n" \
           "void sequence() {"
    return stp

def state_change(channel_states):
    """Code to change pulsebox channel state by writing into `REG_PIOC_ODSR`.
    
    Args:
        * channel_states(iterable of ints): Channel states - 1 or 0.
            This iterable must contain as many values as there are
            pulsebox channels.
    
    Returns:
        * str chng: A piece of code responsible for writing a binary number
            into the `REG_PIOC_ODSR` to achieve the desired state change.
    """
    if len(channel_states) != config.pulsebox_pincount:
        raise ValueError("Incorrect number of channel states given.")
    
    # See what channels are being set to high. What pins correspond to them?
    high_pins = [pin for channel, pin in enumerate(config.pulsebox_pins)
                 if channel_states[channel] == 1]

    # Calculate the value of `REG_PIOC_ODSR`.
    # Start with a binary number full of zeros.
    # For every pin that must be set to high,
    # flip the corresponding bit.
    odsr_value = bin(reduce(lambda x, y: x ^ (1 << y), high_pins, 0))
    
    chng = f"   REG_PIOC_ODSR = {odsr_value};"
    return chng

def loop(iters, loop_suffix="0"):
    """Code containing an inline assembly loop responsible for delay.
    
    Args:
        * iters (int): The number of loop iterations.
    
    Kwargs:
        * loop_suffix (str): The suffix for ASM loop label.
            Default: "0"

    Returns:
        * str asm_loop: The code containing the ASM delay loop.
    
    Notes:
        * Please ensure that throughout your .ino code the individual
            loops have unique identifiers (suffixes).
            The .ino code won't compile otherwise!
    """
    # Check if `iters` is int. If not, attempt conversion (if safe).
    if type(iters) is not int:
        try:
            assert int(iters) == iters
            iters = int(iters)
        except (ValueError, AssertionError):
            raise TypeError("Loop iteration count `iters` is not an int.")

    # Check that `iters` is a valid 32-bit unsigned int.
    # Also, forbid zero-iteration loops.
    if not 0 <= iters < 2**32:
        raise ValueError("Iteration count is not a valid 32-bit unsigned int.")
    if iters == 0:
        raise ValueError("Zero-iteration loops are forbidden.")

    # We fill a 32-bit loop counter register in two steps.
    # First goes the lower 16-bit half, then the top 16-bit half.
    # We need to split the number into two 16-bit halfs, then convert to hex.
    
    top, bottom = [*map(hex, divmod(iters, 65536))]
    asm_loop = "   asm volatile (\n" \
               f'      "MOVW R1, #{bottom}\\n"\n' \
               f'      "MOVT R1, #{top}\\n"\n' \
               f'      "LOOP{loop_suffix}:\\n\\t"\n' \
               '      "NOP\\n\\t"\n' \
               '      "SUB R1, #1\\n\\t"\n' \
               '      "CMP R1, #0\\n\\t"\n' \
               f'      "BNE LOOP{loop_suffix}\\n"\n' \
               "   );"
    return asm_loop

def end():
    """The ending of the .ino source code.
    Contains an empty `loop()` function.
    
    Returns:
        * tail: The ending of the .ino source code.
    """
    tail = "}\n\n" \
           "void loop() {\n" \
           "   ;\n" \
           "}"
    return tail
