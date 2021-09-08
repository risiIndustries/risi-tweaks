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
    "Adwaita": ["#3584e4", "#15539e"],
    "Adwaita-green": ["#2ec27e", "#1a7048"],
    "Adwaita-orange": ["#ff7800", "#994800"],
    "Adwaita-pink": ["#ff00c7", "#990077"],
    "Adwaita-purple": ["#9141ac", "#532562"],
    "Adwaita-red": ["#ed333b", "#ab0f16"],
    "Adwaita-brown": ["#986a44", "#523924"]
}
risiThemes = list(risiColors.keys())
for risicolor in risiThemes.copy():
    risiThemes.append(risicolor + "-dark")


class ThemeSelectionWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.set_vexpand(False)

        # self.stackswitcher = Gtk.StackSwitcher()
        # self.stack = Gtk.Stack()

        self.add(AccentFlowBox(risiColors, 0))
        # self.add(self.stackswitcher)


class OfficialThemePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.set_vexpand(False)

        self.colorint = 0
        self.setting = RtBaseWidgets.known_schemas["org.gnome.desktop.interface"]
        #self.setting.get_string("gtk-theme") in risiThemes and self.setting.get_string("gtk-theme").endswith("-dark")


class AccentFlowBox(Gtk.ScrolledWindow):
    def __init__(self, colors, colorint):
        Gtk.ScrolledWindow.__init__(self)
        self.colors = colors
        self.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.NEVER
        )
        self.set_hexpand(True)
        self.set_vexpand(False)

        self.setting = RtBaseWidgets.known_schemas["org.gnome.desktop.interface"]

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_margin_start(10)
        self.flowbox.set_margin_end(10)
        self.flowbox.set_margin_top(10)
        self.flowbox.set_margin_bottom(10)
        for color in self.colors:
            self.flowbox.add(AccentButton(colors[color][colorint]))

        self.flowbox.connect("child-activated", self.child_activated)
        self.setting.connect("changed", self.setting_changed)

        self.add(self.flowbox)

    def setting_changed(self, setting, key):
        if key == "org.gnome.desktop.interface":
            if self.setting.get_string("gtk-theme") in risiThemes and self.setting.get_string("gtk-theme").endswith("-dark"):
                # if self.flowbox.get_selected_children()[0] == self.flowbox.get_child_at_index(
                #         self.colors.index(self.setting.get_string("gtk-theme")[len(self.setting.get_string("gtk-theme")) - 5])
                # ):
                self.flowbox.select_child(
                    self.flowbox.get_child_at_index(
                        self.colors.keys.index(self.setting.get_string("gtk-theme")[len(self.setting.get_string("gtk-theme")) - 5])
                    )
                )
            elif self.setting.get_string("gtk-theme") in risiThemes:
                # if self.flowbox.get_selected_children()[0] == self.flowbox.get_child_at_index(
                #         self.colors.index(self.setting.get_string("gtk-theme"))
                # ):
                self.flowbox.select_child(
                    self.flowbox.get_child_at_index(
                        self.colors.keys.index(self.setting.get_string("gtk-theme"))
                    )
                )

    def child_activated(self, flowbox, child):
        if self.setting.get_string("gtk-theme") in risiThemes and self.setting.get_string("gtk-theme").endswith("-dark"):
            self.setting.set_string(
                "gtk-theme",
                list(self.colors.keys())[
                    self.flowbox.get_selected_children()[0].get_index()
                ] + "-dark"
            )
        elif self.setting.get_string("gtk-theme") in risiThemes:
            print(list(self.colors.keys()))
            self.setting.set_string(
                "gtk-theme",
                list(self.colors.keys())[
                    self.flowbox.get_selected_children()[0].get_index()
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
        self.set_size_request(8, 8)
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
