#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import pulsebox.sequences as pseq


class ReadTimeTest(unittest.TestCase):
    """Tests for the `read_time` function
    """
    def test_empty_string(self):
        with self.assertRaises(ValueError):
            pseq.read_time("")

    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            pseq.read_time("100x")
        with self.assertRaises(ValueError):
            pseq.read_time("100")

    def test_negative_time(self):
        with self.assertRaises(ValueError):
            pseq.read_time("-100u")
