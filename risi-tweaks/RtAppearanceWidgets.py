# This file contains all the widgets that used for the accent color feature used in Appearance
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RtBaseWidgets
import math

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

risiColors = {
    "Adwaita": "#3584e4",
    "Adwaita-green": "#2ec27e",
    "Adwaita-orange": "#ff7800",
    "Adwaita-pink": "#ff00c7",
    "Adwaita-purple": "#9141ac",
    "Adwaita-red": "#ed333b",
    "Adwaita-brown": "#986a44"
}
risiThemes = list(risiColors.keys())
for risicolor in risiThemes.copy():
    risiThemes.append(risicolor + "-dark")


class ThemeSelectionWidget(Gtk.Revealer):
    def __init__(self):
        Gtk.Revealer.__init__(self)

        self.setting = RtBaseWidgets.known_schemas["org.gnome.desktop.interface"]
        self.setting.connect("changed", self.setting_changed)

        self.set_reveal_child(self.setting.get_string("gtk-theme") in risiThemes)

        self.set_vexpand(False)
        self.box = Gtk.Box()

        #self.box.add(DarkModeToggle)
        self.box.add(AccentFlowBox(risiColors))
        self.add(self.box)
        
    def setting_changed(self, setting, key):
        if key == "gtk-theme":
            self.set_reveal_child(self.setting.get_string("gtk-theme") in risiThemes)


class AccentFlowBox(Gtk.FlowBox):
    def __init__(self, colors):
        Gtk.FlowBox.__init__(self)
        self.colors = colors
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.set_valign(Gtk.Align.START)
        self.setting = RtBaseWidgets.known_schemas["org.gnome.desktop.interface"]

        self.set_margin_top(10)
        self.set_margin_bottom(10)
        for color in self.colors:
            self.add(AccentButton(colors[color]))
            
        self.setting.get_string("gtk-theme")

        self.connect("selected-children-changed", self.child_activated)
        self.setting.connect("changed", self.setting_changed)

        if self.setting.get_string("gtk-theme") in risiThemes and self.setting.get_string("gtk-theme").endswith("-dark"):
            self.select_child(
                self.get_child_at_index(
                    list(self.colors.keys()).index(self.setting.get_string("gtk-theme")[:-5])
                )
            )
        elif self.setting.get_string("gtk-theme") in risiThemes:
            self.select_child(
                self.get_child_at_index(
                    list(self.colors.keys()).index(self.setting.get_string("gtk-theme"))
                )
            )

    def setting_changed(self, setting, key):
        if key == "gtk-theme":
            if self.setting.get_string("gtk-theme") in risiThemes and self.setting.get_string("gtk-theme").endswith("-dark"):
                self.select_child(
                    self.get_child_at_index(
                        list(self.colors.keys()).index(self.setting.get_string("gtk-theme")[:-5])
                    )
                )
            elif self.setting.get_string("gtk-theme") in risiThemes:
                self.select_child(
                    self.get_child_at_index(
                        list(self.colors.keys()).index(self.setting.get_string("gtk-theme"))
                    )
                )

    def child_activated(self, flowbox):
        if self.setting.get_string("gtk-theme") in risiThemes and self.setting.get_string("gtk-theme").endswith("-dark"):
            self.setting.set_string(
                "gtk-theme",
                list(self.colors.keys())[
                    self.get_selected_children()[0].get_index()
                ] + "-dark"
            )
        elif self.setting.get_string("gtk-theme") in risiThemes:
            self.setting.set_string(
                "gtk-theme",
                list(self.colors.keys())[
                    self.get_selected_children()[0].get_index()
                ]
            )


class AccentButton(Gtk.DrawingArea):
    def __init__(self, color):
        Gtk.DrawingArea.__init__(self)
        self.rgba = Gdk.RGBA()
        self.rgba.parse(color)

        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_valign(Gtk.Align.START)
        self.set_size_request(16, 32)
        self.connect("draw", on_draw, {"color": self.rgba})


# Code Stolen from https://python-gtk-3-tutorial.readthedocs.io/en/latest/layout.html to render color
def on_draw(widget, cr, data):
    context = widget.get_style_context()

    width = widget.get_allocated_width()
    height = widget.get_allocated_height()
    Gtk.render_background(context, cr, 0, 0, width, height)

    r, g, b, a = data["color"]
    cr.set_source_rgba(r, g, b, a)
    cr.rectangle(0, 0, width, height)
    cr.fill()
