#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gui.py
A GUI for the Arduino Due pulsebox.

Radim Hošák <hosak(at)optics.upol.cz>
2021 Quantum Optics Lab Olomouc
"""

import csv

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

import os

import pulsebox.config as pcfg
import pulsebox.events as pev
import pulsebox.sequences as pseq


class ChannelEntry(Gtk.Entry):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.set_hexpand(True)


class ChannelToggleButton(Gtk.ToggleButton):
    def __init__(self, channel):
        starts_activated = True if channel == 0 else False
        super().__init__(label=f"CH {channel}", active=starts_activated)
        self.channel = channel


class PulseboxToolbar(Gtk.Toolbar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # self.load_seq_button = Gtk.ToolButton(label="Load sequence")
        # self.save_seq_button = Gtk.ToolButton(label="Save sequence")
        self.parse_seq_button = Gtk.ToolButton(label="Parse sequence")
        # self.quick_upload_button = Gtk.ToolButton(label="Quick upload")
        self.make_ino_button = Gtk.ToolButton(label="Make .ino")
        self.config_button = Gtk.ToolButton(label="Configure")

        # self.insert(self.load_seq_button, -1)
        # self.insert(self.save_seq_button, -1)
        self.insert(self.parse_seq_button, -1)
        self.insert(Gtk.SeparatorToolItem(), -1)
        # self.insert(self.quick_upload_button, -1)
        self.insert(self.make_ino_button, -1)
        self.insert(self.config_button, -1)

        # self.pack_start(self.parse_seq_button, False, False, 0)

class PulseboxHeaderBar(Gtk.HeaderBar):
    def __init__(self):
        super().__init__(title="Pulsebox")
        self.set_show_close_button(True)
        load_image = Gtk.Image.new_from_icon_name("document-open",
                                                  Gtk.IconSize.BUTTON)
        save_image = Gtk.Image.new_from_icon_name("document-save",
                                                  Gtk.IconSize.BUTTON)


        self.load_button = Gtk.Button()
        self.save_button = Gtk.Button()
        self.quick_upload_button = Gtk.Button(label="Quick upload")

        self.load_button.add(load_image)
        self.save_button.add(save_image)

        self.box = Gtk.Box(orientation="horizontal")
        self.box.add(self.load_button)
        self.box.add(self.save_button)
        self.pack_start(self.box)
        self.pack_end(self.quick_upload_button)


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pulsebox", resizable=True)
        self.set_default_size(800, 600)

        self.headerbar = PulseboxHeaderBar()
        self.headerbar.load_button.connect("clicked", self.load_seq)
        self.headerbar.save_button.connect("clicked", self.save_seq)
        self.headerbar.quick_upload_button.connect("clicked", self.quick_upload)
        self.set_titlebar(self.headerbar)

        # self.entry_changed = False

        # self.set_resizable(False)

        self.outer_vbox = Gtk.Box(orientation="vertical", expand=False,
                                  homogeneous=False)

        self.toolbar = PulseboxToolbar(self)

        self.toolbar.parse_seq_button.connect("clicked", self.parse_seq)
        self.toolbar.make_ino_button.connect("clicked", self.make_ino)
        self.toolbar.config_button.connect("clicked", self.config)

        self.hpaned = Gtk.HPaned()
        self.hpaned.set_position(400)
        self.entry_grid = Gtk.Grid(column_homogeneous=False)
        self.channel_toggles = []
        self.channel_entries = []
        for ch in range(pcfg.pulsebox_pincount):
            toggle = ChannelToggleButton(ch)
            toggle.connect("toggled", self.set_entry_changed)
            entry = ChannelEntry(ch)
            entry.connect("changed", self.set_entry_changed)
            self.channel_toggles.append(toggle)
            self.channel_entries.append(entry)
            self.entry_grid.attach(self.channel_toggles[-1], 0, ch, 1, 1)
            self.entry_grid.attach(self.channel_entries[-1], 1, ch, 1, 1)
        self.channel_entries[0].set_text("p1u3u p5u2u p8u1u")
        self.hpaned.add1(self.entry_grid)

        seq_scrolled = Gtk.ScrolledWindow()
        seq_vbox = Gtk.Box(orientation="vertical")
        self.seq_details_label = Gtk.Label()
        self.seq_details_label.set_text("Start by loading/parsing a sequence.")
        seq_vbox.pack_start(self.seq_details_label, False, False, 0)
        self.seq_textbuf = Gtk.TextBuffer()

        code_scrolled = Gtk.ScrolledWindow()
        self.code_textbuf = Gtk.TextBuffer()
        self.code_textbuf.set_text("Start by loading/parsing a sequence.")

        self.seq_textview = Gtk.TextView.new_with_buffer(self.seq_textbuf)
        self.seq_textview.set_sensitive(False)
        seq_scrolled.add(self.seq_textview)

        seq_vbox.pack_end(seq_scrolled, True, True, 0)

        self.code_textview = Gtk.TextView.new_with_buffer(self.code_textbuf)
        # self.code_textview.set_sensitive(False)
        code_scrolled.add(self.code_textview)

        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.append_page(seq_vbox)
        self.notebook.set_tab_label_text(seq_vbox, "Sequence details")
        self.notebook.append_page(code_scrolled)
        self.notebook.set_tab_label_text(code_scrolled, "Source code")
                                  # Gtk.Label("Sequence Details"))

        # self.stack_vbox = Gtk.VBox(homogeneous=False, expand=False)
        # self.stack = Gtk.Stack()
        # self.stack_switcher = Gtk.StackSwitcher(expand=False)
        # self.stack_switcher.set_stack(self.stack)
        # self.stack.add_titled(self.seq_scrolled, name="text", title="Foo")
        # self.stack.show()
        # self.stack_vbox.add(self.stack_switcher)
        # self.stack_vbox.add(self.stack)

        # self.hpaned.add2(self.seq_scrolled)
        self.hpaned.add2(self.notebook)

        self.statusbar = Gtk.Statusbar()
        self.statusbar.push(0, "Ready.")

        self.outer_vbox.pack_start(self.toolbar, False, True, 0)
        self.outer_vbox.pack_start(self.hpaned, False, True, 0)
        # self.outer_vbox.pack_start(self.entry_grid, True, True, 0)
        self.outer_vbox.pack_start(self.statusbar, False, True, 0)
        self.add(self.outer_vbox)

        self.set_entry_changed(self)

    def get_enabled_entries(self):
        return [entry for toggle, entry in zip(self.channel_toggles,
                                               self.channel_entries) \
                if toggle.get_active() == True]

    def unset_entry_changed(self):
        self.entry_changed = False
        self.toolbar.parse_seq_button.set_sensitive(False)

    def set_entry_changed(self, widget):
        self.entry_changed = True
        self.toolbar.parse_seq_button.set_sensitive(True)

    def load_seq(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Load sequence file",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
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

        src_file = dialog.get_filename()
        dialog.destroy()

        for toggle in self.channel_toggles:
            toggle.set_active(False)

        with open(src_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                ch, entry = int(row[0]), " ".join(row[1:])
                print(ch, type(ch))
                print(entry, type(entry))
                self.channel_entries[ch].set_text(entry)
                self.channel_toggles[ch].set_active(True)

        self.statusbar.push(0, f"Loaded sequence from {src_file}.")

        return self.parse_seq(self)

    def save_seq(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Save sequence file",
            parent=self,
            action=Gtk.FileChooserAction.SAVE
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

        dest_file = dialog.get_filename()
        dialog.destroy()

        with open(dest_file, "w") as f:
            writer = csv.writer(f)
            enabled_entries = self.get_enabled_entries()
            for entry in enabled_entries:
                row = [entry.channel] + entry.get_text().split(" ")
                writer.writerow(row)

        self.statusbar.push(0, f"Sequence saved at {dest_file}.")

        return dest_file

    def parse_seq(self, widget):
        self.unset_entry_changed()

        enabled_entries = self.get_enabled_entries()
        flips = []
        for entry in enabled_entries:
            entry_text = entry.get_text()
            new_flips = pev.parse_events(entry_text, entry.channel)
            for flip in new_flips:
                flips.append(flip)
        fs = pseq.FlipSequence(flips)
        seq = pseq.Sequence.from_flip_sequence(fs)
        code = seq.code()

        self.seq_details_label.set_text(f"Duration: {seq.time}\n" \
                                        f"Loops: {seq.loop_counter}")

        self.seq_textbuf.set_text(seq.__repr__())
        self.code_textbuf.set_text(code)
        return seq

    def quick_upload(self, widget):
        seq = self.parse_seq(self)
        code = seq.code()
        dest_dir = "tmp_ino"
        dest_file = os.path.join(dest_dir, "tmp_ino.ino")


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

        enabled_entries = self.get_enabled_entries()
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

    def config(self, widget):
        pass


window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
