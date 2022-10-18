# This file contains all the widgets that used for the accent color feature used in Appearance
# Licensed Under GPL3
# By PizzaLovingNerd
import os

import gi
import rthemelib

import RtBaseWidgets
import RtColorWindow
import adwcolor.functions

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, Gio

settings = Gio.Settings.new("io.risi.rtheme")


class VariantStack(Gtk.Stack):
    def __init__(self):
        Gtk.Stack.__init__(self)
        self.set_transition_duration(0)
        settings.connect("changed::theme-name", self.theme_changed)

        self.add_named(VariantDropdown(), "dropdown")
        self.add_named(AccentColors(), "color")

    def start_function(self):
        self.theme_changed(None, None)
        self.set_transition_duration(500)

    def theme_changed(self, setting, key):
        if settings.get_string("theme-name") == "risi":
            self.set_transition_type(Gtk.StackTransitionType.SLIDE_UP)
            self.set_visible_child_name("color")
        else:
            self.set_transition_type(Gtk.StackTransitionType.SLIDE_DOWN)
            self.set_visible_child_name("dropdown")


class VariantDropdown(RtBaseWidgets.DropdownGSetting):
    def __init__(self):
        super().__init__(
            "rTheme Variant",
            "io.risi.rtheme",
            "variant-name",
            [], []
        )
        self.setting.connect("changed", self.on_setting_changed)
        self.change_theme = False
        self.gen_menu()

    def dropdown_changed(self, dropdown, key, case):
        if self.change_theme:
            self.change_theme = False
            self.setting.set_string(key, self.dropdown.get_active_text())
            self.change_theme = True

    def gen_menu(self):
        self.change_theme = False
        variants = rthemelib.get_current_theme().variants
        for variant in variants:
            self.case.append(variant.name)
            self.menu.append(variant.name)

        for entry in self.menu:  # Adds items to dropdown
            self.dropdown.append_text(entry)

        if self.setting.get_string("variant-name") in self.case:
            self.dropdown.set_active(self.case.index(self.setting.get_string("variant-name")))
        else:
            self.dropdown.set_active(0)
        self.change_theme = True

    def on_setting_changed(self, setting, changed_key):
        if changed_key == "theme-name":
            self.change_theme = False
            self.dropdown.remove_all()
            self.case = []
            self.menu = []
            self.gen_menu()
        if self.setting.get_string("theme-name") == "risi":
            background = Gio.Settings("org.gnome.desktop.background")
            if background.get_string("picture-uri").startswith("file:///usr/share/backgrounds/risios-37/37-"):
                color = settings.get_string("variant-name")
                if color == "main":
                    color = "blood-orange"

                background.set_string(
                    "picture-uri", f"file:///usr/share/backgrounds/risios-37/37-light-{color}.png"
                )
                background.set_string(
                    "picture-uri-dark", f"file:///usr/share/backgrounds/risios-37/37-dark-{color}.png"
                )

colors = ["main", "blue", "green", "orange", "yellow", "red", "purple", "brown"]

color_previews = {
    "main": "#ed4a3f",
    "blue": "#1c71d8",
    "green": "#2ec27e",
    "orange": "#e66100",
    "yellow": "#f5c211",
    "red": "#c01c28",
    "purple": "#813d9c",
    "brown": "#865e3c"
}


class AccentColors(RtBaseWidgets.Option):
    def __init__(self):
        RtBaseWidgets.Option.__init__(self, "Accent Colors")
        self.add(AccentFlowBox())
        self.set_vexpand(False)
        self.set_valign(Gtk.Align.START)
        self.label.set_hexpand(False)
        self.label.set_halign(Gtk.Align.START)
        self.set_margin_end(10)


class AccentFlowBox(Gtk.FlowBox):
    def __init__(self):
        Gtk.FlowBox.__init__(self)
        self.set_vexpand(False)
        self.set_valign(Gtk.Align.START)
        self.set_hexpand(True)
        self.set_halign(Gtk.Align.END)
        self.set_homogeneous(True)

        for color in colors:
            self.add(AccentButton(color))
            try:
                self.select_child(
                    self.get_child_at_index(
                        colors.index(settings.get_string("variant-name"))
                    )
                )
            except TypeError:
                self.select_child(self.get_child_at_index(0))
        self.set_max_children_per_line(len(colors))

        self.connect("selected-children-changed", self.child_activated)
        settings.connect("changed::variant-name", self.on_setting_changed)

    def child_activated(self, flowbox):
        try:
            settings.set_string("variant-name", colors[flowbox.get_selected_children()[0].get_index()])
        except ValueError:
            pass

    def on_setting_changed(self, setting, key):
        try:
            self.select_child(
                self.get_child_at_index(
                    colors.index(settings.get_string("variant-name"))
                )
            )
        except TypeError:
            self.select_child(self.get_child_at_index(0))


class AccentButton(Gtk.DrawingArea):
    def __init__(self, color):
        Gtk.DrawingArea.__init__(self)
        self.rgba = Gdk.RGBA()
        self.rgba.parse(color_previews[color])

        self.set_margin_start(3)
        self.set_margin_end(3)
        self.set_margin_top(3)
        self.set_margin_bottom(3)
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.CENTER)
        self.set_hexpand(False)
        self.set_size_request(16, 16)
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

