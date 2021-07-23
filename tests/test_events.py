#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import pulsebox.events as pev


class ReadTimeTest(unittest.TestCase):
    """Tests for the `read_time` function
    """
    def test_empty_string(self):
        with self.assertRaises(ValueError):
            pev.read_time("")

    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            pev.read_time("100x")
        with self.assertRaises(ValueError):
            pev.read_time("100")

    def test_negative_time(self):
        with self.assertRaises(ValueError):
            pev.read_time("-100u")
