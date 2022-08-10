# Loads up main window
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RtBaseWidgets
import adwcolor.functions
import adwcolor.properties

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio

settings = Gio.Settings.new("org.gnome.desktop.interface")


class Color:
    def __init__(self, color_name, color_label, color_default_light, color_default_dark):
        self.color_name = color_name
        self.color_label = color_label
        self.color_default_light = color_default_light
        self.color_default_dark = color_default_dark

    def get_new_color_widget(self):
        return ColorWidget(
            self.color_name, self.color_label,
            self.color_default_light, self.color_default_dark
        )


colors = [
    Color("accent_color", "Accent Color", "#1c71d8", "#78aeed"),
    Color("accent_bg_color", "Accent Background Color", "#3584e4", "#3584e4"),
    Color("accent_fg_color", "Accent Foreground Color", "#ffffff", "#ffffff"),
    Color("destructive_color", "Destructive Color", "#c01c18", "#ff7b63"),
    Color("destructive_bg_color", "Destructive Background Color", "#e01b24", "#c01c28"),
    Color("destructive_fg_color", "Destructive Foreground Color", "#ffffff", "#ffffff"),
    Color("success_color", "Success Color", "#26a269", "#8ff0a4"),
    Color("success_bg_color", "Success Background Color", "#2ec27e", "#26a269"),
    Color("success_fg_color", "Success Foreground Color", "#ffffff", "#ffffff"),
    Color("warning_color", "Warning Color", "#ae7b03", "#f8e45c"),
    Color("warning_bg_color", "Warning Background Color", "#a5a50a", "#cd9309"),
    Color("warning_fg_color", "Warning Foreground Color", "rgba(0, 0, 0, 0.8)", "rgba(0, 0, 0, 0.8)"),
    Color("error_color", "Error Color", "#c01c18", "#ff7b63"),
    Color("error_bg_color", "Error Background Color", "#e01b24", "#c01c28"),
    Color("error_fg_color", "Error Foreground Color", "#ffffff", "#ffffff"),
    Color("window_bg_color", "Window Background Color", "#fafafa", "#242424"),
    Color("window_fg_color", "Window Foreground Color", "rgba(0, 0, 0, 0.8)", "rgba(0, 0, 0, 0.8)"),
    Color("window_bg_color", "View Background Color", "#ffffff", "#1e1e1e"),
    Color("window_fg_color", "View Foreground Color", "#000000", "ffffff"),
    Color("headerbar_bg_color", "Headerbar Background Color", "#ebebeb", "#303030"),
    Color("headerbar_fg_color", "Headerbar Foreground Color", "rgba(0, 0, 0, 0.8)", "#ffffff"),
    Color("headerbar_border_color", "Headerbar Border Color", "rgba(0, 0, 0, 0.8)", "#ffffff"),
    Color("headerbar_backdrop_color", "Headerbar Backdrop Color", "#fafafa", "#242424"),
    Color("headerbar_share_color", "Headerbar Share Color", "rgba(0, 0, 0, 0.07)", "rgba(0, 0, 0, 0.36)"),
    Color("card_bg_color", "Card Background Color", "#ffffff", "rgba(255, 255, 255, 0.08)"),
    Color("card_fg_color", "Card Foreground Color", "rgba(0, 0, 0, 0.8)", "#ffffff"),
    Color("card_shade_color", "Card Shade Color", "rgba(0, 0, 0, 0.07)", "rgba(0, 0, 0, 0.36)"),
    Color("dialog_bg_color", "Dialog Background Color", "#fafafa", "#282828"),
    Color("dialog_fg_color", "Dialog Foreground Color", "rgba(0, 0, 0, 0.8)", "#ffffff"),
    Color("popover_bg_color", "Popover Background Color", "#ffffff", "#383838"),
    Color("popover_fg_color", "Popover Foreground Color", "rgba(0, 0, 0, 0.8)", "#ffffff"),
    Color("shade_color", "Popover Shade Color", "rgba(0, 0, 0, 0.07)", "rgba(0, 0, 0, 0.36)"),
    Color("scrollbar_outline_color", "Scrollbar Outline Color", "#ffffff", "rgba(0, 0, 0, 0.5)"),
]


class ColorWidget(RtBaseWidgets.Option):
    def __init__(self, color_name, color_label, color_default_light, color_default_dark):
        self.color_default = None
        self.edit_mode = False
        super().__init__(color_label)
        self.color_name = color_name

        self.color_default_light = color_default_light
        self.color_default_dark = color_default_dark

        settings.connect("changed", self.settings_set)

        # Add color picker
        self.color_picker = Gtk.ColorButton()
        self.color_picker.connect("color-set", self.apply)
        self.color_picker.set_margin_end(10)

        # Thanks GNOME for making me do this...
        Gtk.ColorChooser.set_use_alpha(self.color_picker, True)

        self.refresh_color_button()

        self.default_button = Gtk.Button()
        self.default_button.set_image(Gtk.Image.new_from_icon_name("view-refresh", Gtk.IconSize.BUTTON))
        self.default_button.set_margin_end(5)
        self.default_button.connect("clicked", self.restore)
        self.add(self.color_picker)
        self.add(self.default_button)

    def settings_set(self, setting, key):
        if key == "color-scheme":
            self.refresh_color_button()

    def apply(self, widget):
        current_color_value = widget.get_rgba().to_string()
        adwcolor.functions.modify(self.color_name, current_color_value)
        self.refresh_color_button()

    def restore(self, widget):
        adwcolor.functions.restore(self.color_name)
        self.refresh_color_button()

    def refresh_color_button(self):
        if settings.get_string("color-scheme") == "prefer-dark":
            self.color_default = self.color_default_dark
        else:
            self.color_default = self.color_default_light

        current_color_value = adwcolor.functions.get_value(self.color_name)
        rgba_color = Gdk.RGBA()
        if current_color_value is not None:
            if current_color_value in adwcolor.properties.palette_colors:
                rgba_color.parse(adwcolor.properties.palette_colors[current_color_value])
            else:
                rgba_color.parse(current_color_value)
        else:
            rgba_color.parse(self.color_default)
        self.color_picker.set_rgba(rgba_color)


# Launches main window of risiTweaks
class RtColorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="risiTweaks Color Customizer")
        self.set_default_size(-1, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("io.risi.tweaks")
        self.set_modal(True)

        # Creating the Header Bar and the two views for the Header Bar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.set_margin_start(10)
        self.box.set_margin_end(10)
        self.box.set_margin_top(10)
        self.box.set_margin_bottom(10)

        label_top = RtBaseWidgets.Label("Color Customization")
        label_bottom = RtBaseWidgets.Description("<small>Only Applies to Gtk3 Apps if adw-gtk3 is set as gtk "
                                                 "theme.\nAll colors will reset when switching between light and dark "
                                                 "mode.\nApplications require restart.</small>")
        label_top.label.set_margin_bottom(0)
        label_bottom.set_margin_bottom(10)

        self.box.add(label_top)
        self.box.add(label_bottom)

        for color in colors:
            self.box.add(color.get_new_color_widget())

        self.scrolled_page = Gtk.ScrolledWindow()  # Creates page in scrolled window
        self.scrolled_page.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_page.add(self.box)
        self.add(self.scrolled_page)