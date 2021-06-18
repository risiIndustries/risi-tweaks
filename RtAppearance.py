# The Appearance Page in the UI category
# UI -> Appearance
# Licensed Under LGPL3
# By PizzaLovingNerd

import gi
import RtSettings
import RtUtils

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RtAppearance(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(RtSettings.Label("Theming:"))
        self.add(
            RtSettings.DropdownSetting(
                "Application Theme",
                "org.gnome.desktop.interface",
                "gtk-theme",
                RtUtils.get_gtk_themes(),
                "same"
            )
        )
        self.add(
            RtSettings.DropdownSetting(
                "Icon Theme",
                "org.gnome.desktop.interface",
                "icon-theme",
                RtUtils.get_icon_themes(),
                "same"
            )
        )
        self.add(
            RtSettings.DropdownSetting(
                "Cursor Theme",
                "org.gnome.desktop.interface",
                "cursor-theme",
                RtUtils.get_cursor_themes(),
                "same"
            )
        )
        self.add(RtSettings.Space(5))
        self.add(RtSettings.Label("Fonts:"))
        self.add(
            RtSettings.FontSetting(
                "Legacy Window Title Font",
                "org.gnome.desktop.wm.preferences",
                "titlebar-font"
            )
        )
        self.add(
            RtSettings.FontSetting(
                "Interface Font",
                "org.gnome.desktop.interface",
                "font-name"
            )
        )
        self.add(
            RtSettings.FontSetting(
                "Document Font",
                "org.gnome.desktop.interface",
                "document-font-name"
            )
        )
        self.add(
            RtSettings.FontSetting(
                "Monospace Font",
                "org.gnome.desktop.interface",
                "monospace-font-name"
            )
        )
        self.add(
            RtSettings.DropdownSetting(
                "Font Hinting",
                "org.gnome.desktop.interface",
                "font-hinting",
                ["Full", "Medium", "Slight", "None"],
                "lower"
            )
        )
        self.add(
            RtSettings.DropdownSetting(
                "Antialiasing",
                "org.gnome.desktop.interface",
                "font-antialiasing",
                ["Subpixel (for LCDs)", "Standard (grayscale)", "None"],
                ["rgba", "grayscale", "none"]
            )
        )
        self.add(
            RtSettings.SpinButtonSetting(
                "Scaling Factor",
                "org.gnome.desktop.interface",
                "text-scaling-factor",
                0.50, 3.00, 0.05, True
            )
        )