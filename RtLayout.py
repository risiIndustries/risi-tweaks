# The Layout Page in the UI category
# UI -> Layout
# Licensed Under LGPL3
# By PizzaLovingNerd

import gi
import RtSettings
import RtUtils

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RtLayout(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        self.MenuSettings = Gtk.Button(label="Placeholder 1")
        self.PanelSettings = Gtk.Button(label="Placeholder 2")
        self.MenuSettings.connect("clicked", self.launch)
        self.PanelSettings.connect("clicked", self.launch)
        self.ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.ButtonBox.add(self.MenuSettings)
        self.ButtonBox.add(self.PanelSettings)

        self.add(RtSettings.Label(
            "Layout"
        ))
        self.add(RtSettings.Dropdown(
            "Desktop Layout (Coming Soon)"
        ))
        self.add(RtSettings.Space(25))
        self.add(RtSettings.Dropdown(
            "Panel Setup (Coming Soon)"
        ))
        self.add(RtSettings.Dropdown(
            "Menu Layout (Coming Soon)"
        ))
        self.add(self.ButtonBox)
        self.add(RtSettings.Space(25))
        self.add(RtSettings.Toggle("Placeholder"))
        self.add(RtSettings.Toggle("Placeholder"))
        self.add(RtSettings.Space(25))
        self.add(RtSettings.ToggleSetting(
            "Activities Hot Corner",
            "org.gnome.desktop.interface",
            "enable-hot-corners"
        ))
        self.add(RtSettings.Label(
            "Clock"
        ))
        self.add(RtSettings.ToggleSetting(
            "Show Seconds",
            "org.gnome.desktop.interface",
            "clock-show-seconds"
        ))
        self.add(RtSettings.ToggleSetting(
            "Show Date",
            "org.gnome.desktop.interface",
            "clock-show-date"
        ))
        self.add(RtSettings.ToggleSetting(
            "Show Week day",
            "org.gnome.desktop.interface",
            "clock-show-weekday"
        ))
        self.add(RtSettings.ToggleSetting(
            "Calendar Week Numbers",
            "org.gnome.desktop.calendar",
            "show-weekdate"
        ))


    def launch(self, button):
        print("placeholder")