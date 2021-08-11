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

import os

import pulsebox.config as pcfg
import pulsebox.events as pev
import pulsebox.sequences as pseq


class ChannelEntry(Gtk.Entry):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.set_hexpand(True)


class ChannelCheckButton(Gtk.CheckButton):
    def __init__(self, channel):
        starts_activated = True if channel == 0 else False
        super().__init__(label=f"CH {channel}", active=starts_activated)
        self.channel = channel


class PulseboxToolbar(Gtk.Toolbar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.make_ino_button = Gtk.ToolButton(label="Make .ino")
        self.insert(self.make_ino_button, -1)


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

        self.toolbar = PulseboxToolbar(self)
        self.toolbar.make_ino_button.connect("clicked", self.make_ino)

        # self.statusbar = Gtk.Statusbar()
        # self.statusbar.push(0, "Ready.")

        self.outer_vbox.pack_start(self.toolbar, True, True, 0)
        self.outer_vbox.pack_start(self.entry_grid, True, True, 0)
        # self.outer_vbox.pack_start(self.statusbar, True, True, 0)
        self.add(self.outer_vbox)

    def make_ino(self, widget):
        # Let the user select the directory for the .ino
        dialog = Gtk.FileChooserDialog(
            title="Create a folder for the .ino project",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)
        response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return

        dest_dir = dialog.get_filename()
        dialog.destroy()

        ino_name = os.path.split(dest_dir)[-1] + ".ino"
        dest_file = os.path.join(dest_dir, ino_name)

        enabled_entries = [entry for toggle, entry \
                           in zip(self.channel_toggles,
                                  self.channel_entries) \
                           if toggle.get_active() == True]
        flips = []
        for entry in enabled_entries:
            entry_text = entry.get_text()
            new_flips = pev.parse_events(entry_text, entry.channel)
            for flip in new_flips:
                flips.append(flip)
        fs = pseq.FlipSequence(flips)
        seq = pseq.Sequence.from_flip_sequence(fs)

        code = seq.code()

        with open(dest_file, "w") as f:
            f.write(code)


window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
