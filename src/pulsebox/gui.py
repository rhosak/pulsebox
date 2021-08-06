#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gui.py
A GUI for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pulsebox.events as pev
import pulsebox.config as pcfg


class ChannelEntry(Gtk.Entry):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.set_hexpand(True)


class ChannelCheckButton(Gtk.CheckButton):
    def __init__(self, channel):
        super().__init__(label=f"CH {channel}", active=True)
        self.channel = channel


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pulsebox", resizable=False)
        # self.set_resizable(False)

        self.outer_vbox = Gtk.Box(orientation="vertical")

        self.entry_grid = Gtk.Grid(column_homogeneous=False)
        self.channel_toggles = []
        self.channel_entries = []
        for ch in range(pcfg.pulsebox_pincount):
            self.channel_toggles.append(ChannelCheckButton(ch))
            self.channel_entries.append(ChannelEntry(ch))
            self.entry_grid.attach(self.channel_toggles[-1], 0, ch, 1, 1)
            self.entry_grid.attach(self.channel_entries[-1], 1, ch, 1, 1)

        self.toolbar = Gtk.Toolbar()
        self.make_ino_button = Gtk.ToolButton(label="Make .ino")
        self.make_ino_button.connect("clicked", make_ino,
                                     self.channel_toggles, self.channel_entries)
        self.toolbar.insert(self.make_ino_button, -1)

        self.statusbar = Gtk.Statusbar()
        self.statusbar.push(0, "Ready.")

        self.outer_vbox.pack_start(self.toolbar, True, True, 0)
        self.outer_vbox.pack_start(self.entry_grid, True, True, 0)
        self.outer_vbox.pack_start(self.statusbar, True, True, 0)
        self.add(self.outer_vbox)

def make_ino(widget, channel_toggles, channel_entries):
    enabled_entries = [entry for toggle, entry \
                       in zip(channel_toggles, channel_entries) \
                       if toggle.get_active() == True]
    for entry in enabled_entries:
        entry_text = entry.get_text()
        pev.parse_events(entry_text, entry.channel)

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
