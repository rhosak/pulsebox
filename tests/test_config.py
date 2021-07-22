#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os.path
from .context import config

class ConfigFileTest(unittest.TestCase):
    """Tests regarding the config file
    """
    
    def test_presence(self):
        self.assertTrue(os.path.isfile("pulsebox/config.ini"),
                        "The config.ini file was not found.")

    def test_pulsebox_section(self):
        self.assertTrue(config.parser.has_section("Pulsebox"),
                        "Pulsebox section missing in the config file.")

    def test_codeblocks_section(self):
        self.assertTrue(config.parser.has_section("CodeBlocks"),
                        "CodeBlocks section missing in the config file.")

    def test_arduino_section(self):
        self.assertTrue(config.parser.has_section("Arduino"),
                        "Arduino section missing in the config file.")


class PulseboxPinsTest(unittest.TestCase):
    """Tests for the `pulsebox_pins` option in the `Pulsebox` section.
    """

    def test_specified(self):
        self.assertTrue(config.parser.has_option("Pulsebox", "pulsebox_pins"),
                        "pulsebox_pins not defined.")

    def test_only_commas_and_numerals(self):
        for char in config.parser.get("Pulsebox", "pulsebox_pins"):
            self.assertIn(char, "0123456789,",
                          "Incorrect format of pulsebox_pins. " \
                          "Expected comma-separated numbers.")

    def test_no_empty_string(self):
        pins = config.parser.get("Pulsebox", "pulsebox_pins")
        split_pins = pins.split(",")
        self.assertFalse("" in split_pins,
                         "Empty string detected when splitting by ','. " \
                         "Probably two consecutive commas or no pins given.")

    def test_at_least_one_pin(self):
        pins = config.parser.get("Pulsebox", "pulsebox_pins")
        split_pins = pins.split(",")
        self.assertTrue(len(split_pins) >= 1, "No pulsebox_pins given")

    def test_correctly_parsed(self):
        pins = config.parser.get("Pulsebox", "pulsebox_pins")
        split_pins = pins.split(",")
        pulsebox_pins = [*map(int, split_pins)]
        self.assertEqual(pulsebox_pins, config.pulsebox_pins,
                         "pulsebox_pins incorrectly parsed by config.py.")

    def test_correct_portC_pins(self):
        forbidden_pins = [10, 11, 20, 27]
        for pin in config.pulsebox_pins:
            self.assertTrue(1 <= pin <= 30,
                            "Pulsebox pin number outside of allowed range.")
            self.assertNotIn(pin, forbidden_pins,
                             "Forbidden PORTC pin found in pulsebox_pins.")
        

class TriggerPinTest(unittest.TestCase):
    """Tests for the `trigger_pin` option in the `Pulsebox` section
    """
    
    def test_specified(self):
        self.assertTrue(config.parser.has_option("Pulsebox", "trigger_pin"),
                        "Trigger pin was not specified.")

    def test_nonempty(self):
        trigger_pin = config.parser.get("Pulsebox", "trigger_pin")
        self.assertNotEqual(trigger_pin, "", "trigger_pin is an empty string.")

    def test_is_int(self):
        trigger_pin = config.parser.get("Pulsebox", "trigger_pin")
        for char in trigger_pin:
            self.assertIn(char, "0123456789",
                          "trigger_pin is not an integer.")

    def test_correctly_parsed(self):
        trigger_pin = config.parser.getint("Pulsebox", "trigger_pin")
        self.assertEqual(trigger_pin, config.trigger_pin,
                         "trigger_pin parsed incorrectly by config.py.")

    def test_valid_pin(self):
        self.assertTrue(0 <= config.trigger_pin <= 78,
                        "trigger_pin is not a valid Arduino Due pin.")

    def test_not_overlapping(self):
        """Check that the trigger pin is not identical to a pulsebox pin.
        """
        self.assertNotIn(config.trigger_pin, config.pulsebox_pins,
                         "Trigger pin identical with pulsebox pin.")


class ContModeDelayMsTest(unittest.TestCase):
    """Tests for the `cont_mode_delay_ms` option in the `Pulsebox` section
    """
    
    def test_specified(self):
        self.assertTrue(config.parser.has_option("Pulsebox",
                                                 "cont_mode_delay_ms"),
                        "cont_mode_delay_ms was not specified.")

    def test_nonempty(self):
        delay = config.parser.get("Pulsebox", "cont_mode_delay_ms")
        self.assertNotEqual(delay, "",
                            "cont_mode_delay_ms is not an empty string.")

    def test_is_int(self):
        delay = config.parser.get("Pulsebox", "cont_mode_delay_ms")
        for char in delay:
            self.assertIn(char, "0123456789",
                          "cont_mode_delay_ms is not an integer.")

    def test_correctly_parsed(self):
        delay = config.parser.getint("Pulsebox", "cont_mode_delay_ms")
        self.assertEqual(delay, config.cont_mode_delay_ms,
                         "cont_mode_delay_ms incorrectly parsed by config.py.")

    def test_valid_32_unsigned_int(self):
        self.assertTrue(0 <= config.cont_mode_delay_ms < 2**32,
                        "cont_mode_delay_ms is not a 32-bit unsigned int.")


class CalibrationTest(unittest.TestCase):
    """Tests for the `calibration` option in the `Pulsebox` section
    """
    
    def test_specified(self):
        self.assertTrue(config.parser.has_option("Pulsebox", "calibration"),
                        "Calibration was not specified.")

    def test_nonempty(self):
        calibration = config.parser.get("Pulsebox", "calibration")
        self.assertNotEqual(calibration, "", "Calibration is an empty string.")


class HeaderTest(unittest.TestCase):
    """Tests for the `header` option in the `CodeBlocks` section
    """
    
    def test_specified(self):
        self.assertTrue(config.parser.has_option("CodeBlocks", "header"),
                        "Header was not specified.")


class PortTest(unittest.TestCase):
    """Tests for the `port` option in the `Arduino` section
    """
    
    def test_specified(self):
        self.assertTrue(config.parser.has_option("Arduino", "port"),
                        "Arduino port was not specified.")

    def test_nonempty(self):
        port = config.parser.get("Arduino", "port")
        self.assertNotEqual(port, "", "Port is an empty string.")


class ByIdStringTest(unittest.TestCase):
    """Tests for the `by_id_string` option in the `Arduino` section.
    
    We allow `by_id_string` to be empty.
    """
    
    def test_specified(self):
        self.assertTrue(config.parser.has_option("Arduino", "by_id_string"),
                        "by_id_string was not specified.")

        

if __name__ == "__main__":
    unittest.main()
