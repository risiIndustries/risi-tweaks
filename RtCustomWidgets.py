# This file contains all the widgets that are for a specific page
# If the page isn't important enough to have it's own file for widgets
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RtBaseWidgets

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

# Used for the "Raise Window When Focused Setting"
# Setting only shows up if the window focus mode is set to "sloppy"
class RaiseWindowWhenFocused(RtBaseWidgets.ToggleGSetting):
    def __init__(self):
        RtBaseWidgets.ToggleGSetting.__init__(
            self,
            "Raise Windows When Focused",
            "org.gnome.desktop.wm.preferences",
            "auto-raise"
        )

        self.setting.connect("changed", self.on_setting_changed)

    # Checks to see if Window focus mode is set to "sloppy" and makes it visible if it is.
    def start_function(self):
        self.set_visible(self.setting.get_string("focus-mode") == "sloppy")

    def on_setting_changed(self, setting, changed_key):
        self.set_visible(self.setting.get_string("focus-mode") == "sloppy")
