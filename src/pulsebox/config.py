#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""config.py
Reads the pulsebox configuration from the config.ini file.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

import configparser
import os

from functools import reduce

# Do not change the configuration here! Instead, use the provided config.ini.
DEFAULTS = {
    "Pulsebox": {
        "pulsebox_pins": "1,3,5,7,9,18,16,14,12,2,4,6,8,19,17,15",
        "trigger_pin": 52,
        "cont_mode_delay_ms": 0,
        "calibration": 6.4e-08
    },
    "CodeBlocks": {
        "header": "Automatically generated file"
    },
    "Arduino": {
        "port": "/dev/ttyACM0",
        "by_id_string": ""
    }
}

parser = configparser.ConfigParser()
parser.read_dict(DEFAULTS)  # load the default configuration

# The values in the config.ini file override the defaults.
# In any scenario, only one of the two paths should contain the file.
# Which of these two it is depends on our working directory.
# If we are running `import config` from the `pulsebox` directory,`config.ini`
# is the correct path. However, when running `import pulsebox.config`
# from the `src` directory, we need to descend into `pulsebox` first.
# We will store the path to the configuration file, just in case we need it.
filename = parser.read(["config.ini",
                       os.path.join("pulsebox", "config.ini")])[0]

pulsebox_pins = [*map(int, parser.get("Pulsebox", "pulsebox_pins").split(","))]
trigger_pin = parser.getint("Pulsebox", "trigger_pin")
cont_mode_delay_ms = parser.getint("Pulsebox", "cont_mode_delay_ms")
calibration = parser.getfloat("Pulsebox", "calibration")
header = parser.get("CodeBlocks", "header")
port = parser.get("Arduino", "port")
by_id_string = parser.get("Arduino", "by_id_string")

# Two convenience variables: pulsebox pin count and a binary value
# corresponding to all pulsebox pins being enabled (set to 1):
pulsebox_pincount = len(pulsebox_pins)
all_pins_enabled = bin(reduce(lambda x, y: x ^ (1 << y), pulsebox_pins, 0))
