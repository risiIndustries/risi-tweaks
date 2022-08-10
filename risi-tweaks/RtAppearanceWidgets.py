# This file contains all the widgets that used for the accent color feature used in Appearance
# Licensed Under GPL3
# By PizzaLovingNerd
import os

import gi
import RtBaseWidgets
import RtColorWindow
import adwcolor.functions

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk


class Theme:
    def __init__(self, props):
        self.props = props

    def apply(self):
        for item in self.props.items():
            adwcolor.functions.modify(item[0], item[1])

    def is_enabled(self):
        for item in self.props.items():
            if not adwcolor.functions.get_value(item[0]) == item[1]:
                return False
        return True


class Default(Theme):
    def __init__(self, props):
        super().__init__({})
        self.props = props

    def apply(self):
        for prop in self.props:
            adwcolor.functions.restore(prop)

    def is_enabled(self):
        if not os.path.exists(f"{os.path.expanduser('~')}/.config/gtk-4.0/gtk.css"):
            return True
        else:
            for item in self.props:
                if adwcolor.functions.get_value(item) is None:
                    return True
        return False


Colors = {
    0: Default(  # Blue (Default)
        ["accent_color", "accent_bg_color", "accent_fg_color"]
    ),
    1: Theme({  # Green
        "accent_color": "@green_4",
        "accent_bg_color": "@green_5",
        "accent_fg_color": "#ffffff"
    }),
    2: Theme({  # Orange
        "accent_color": "@orange_4",
        "accent_bg_color": "@orange_5",
        "accent_fg_color": "#ffffff"
    }),
    3: Theme({  # Yellow
        "accent_color": "@yellow_4",
        "accent_bg_color": "@yellow_5",
        "accent_fg_color": "#ffffff"
    }),
    4: Theme({  # Red
        "accent_color": "@red_4",
        "accent_bg_color": "@red_5",
        "accent_fg_color": "#ffffff"
    }),
    5: Theme({  # Purple
        "accent_color": "@purple_4",
        "accent_bg_color": "@purple_5",
        "accent_fg_color": "#ffffff"
    }),
    6: Theme({  # Brown
        "accent_color": "@brown_4",
        "accent_bg_color": "@brown_5",
        "accent_fg_color": "#ffffff"
    })
}
Preview_Colors = {
    "@green_5": "#33d17a",
    "@orange_5": "#ff7800",
    "@yellow_5": "#f5c211",
    "@red_5": "#e01b24",
    "@purple_5": "#9141ac",
    "@brown_5": "#986a44"
}


class Custom(Theme):
    def __init__(self):
        super().__init__({})

    def apply(self):
        pass

    def is_enabled(self):
        for color in Colors.values():
            if color.is_enabled():
                return False
        return True


class AccentColors(RtBaseWidgets.Option):
    def __init__(self):
        RtBaseWidgets.Option.__init__(self, "Accent Colors: ")
        self.add(AccentFlowBox(Colors))
        self.set_margin_top(10)
        self.set_margin_end(5)


class AccentFlowBox(Gtk.FlowBox):
    def __init__(self, colors):
        Gtk.FlowBox.__init__(self)
        self.colors = colors
        self.set_vexpand(False)
        self.set_valign(Gtk.Align.START)
        self.set_min_children_per_line(100)
        self.set_size_request(-1, 30)

        for color in self.colors:
            self.add(AccentButton(colors[color]))
            if colors[color].is_enabled():
                self.select_child(self.get_child_at_index(color))

        self.connect("selected-children-changed", self.child_activated)

    def child_activated(self, flowbox):
        self.colors[flowbox.get_selected_children()[0].get_index()].apply()


class AccentButton(Gtk.DrawingArea):
    def __init__(self, color):
        Gtk.DrawingArea.__init__(self)
        self.rgba = Gdk.RGBA()
        if isinstance(color, Default):
            self.rgba.parse("#3584e4")
        else:
            self.rgba.parse(Preview_Colors[color.props["accent_bg_color"]])

        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(5)
        self.set_margin_bottom(5)
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.CENTER)
        self.set_hexpand(False)
        self.set_size_request(16, 16)
        self.connect("draw", on_draw, {"color": self.rgba})


class CustomColorsButton(RtBaseWidgets.Option):
    def __init__(self, application):
        RtBaseWidgets.Description.__init__(self, "Incompatible with non adw-gtk3 themes, applications require restart.")

        self.application = application
        self.window = RtColorWindow.RtColorWindow(self.application)
        self.window.set_destroy_with_parent(True)
        self.application.add_window(self.window)

        button = Gtk.Button(label="Custom Colors")
        button.connect("clicked", self.launch_custom_colors)
        self.set_margin_end(5)
        self.set_margin_bottom(10)
        self.add(button)

    def launch_custom_colors(self, widget):
        self.window.show_all()
        self.window.set_transient_for(self.get_toplevel())

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

