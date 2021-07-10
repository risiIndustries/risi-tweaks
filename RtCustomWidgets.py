import os
import gi

import RtUtils
import RtBaseWidgets

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class RaiseWindowWhenFocused(RtBaseWidgets.ToggleGSetting):
    def __init__(self):
        RtBaseWidgets.ToggleGSetting.__init__(
            self,
            "Raise Windows When Focused",
            "org.gnome.desktop.wm.preferences",
            "auto-raise"
        )

        self.setting.connect("changed", self.on_setting_changed)

    def start_function(self):
        self.set_visible(self.setting.get_string("focus-mode") == "sloppy")

    def on_setting_changed(self, setting, changed_key):
        self.set_visible(self.setting.get_string("focus-mode") == "sloppy")