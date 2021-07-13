# This file is a place to put extra functions for risiTweaks
# so that we don't have a bunch of random functions at the
# bottom of all our classes
# Licensed Under LGPL3
# By PizzaLovingNerd

import os
from gi.repository import Gio

_HOME = os.getenv("HOME")


def check_dir_for_file_to_list(input_list, directory, file_check):
    if os.path.isdir(directory):
        for item in os.listdir(directory):
            if item not in input_list and os.path.isdir(directory + "/" + item) \
                    and os.path.exists(directory + item + file_check):
                input_list.append(item)
    return input_list


def check_dir_for_icon_theme(input_list, directory, file_check):
    if os.path.isdir(directory):
        for item in os.listdir(directory):
            if item not in input_list and os.path.isdir(directory + "/" + item) \
                    and os.path.exists(directory + item + file_check):
                icon_theme_dirs = []
                for item1 in os.listdir(directory + item):
                    if os.path.isdir(directory + item + "/" + item1):
                        icon_theme_dirs = [item1]
                if icon_theme_dirs != [] and icon_theme_dirs != ["cursors"]:
                    input_list.append(item)
    return input_list


def get_gtk_themes():
    gtk_themes = []

    gtk_themes = check_dir_for_file_to_list(
        gtk_themes,
        "/usr/share/themes/",
        "/gtk-3.0/gtk.css"
    )

    gtk_themes = check_dir_for_file_to_list(
        gtk_themes,
        _HOME + "/.themes/",
        "/gtk-3.0/gtk.css"
    )

    gtk_themes = check_dir_for_file_to_list(
        gtk_themes,
        _HOME + "/.local/share/themes/",
        "/gtk-3.0/gtk.css"
    )

    return gtk_themes


def get_icon_themes():
    icon_themes = []

    icon_themes = check_dir_for_icon_theme(
        icon_themes,
        "/usr/share/icons/",
        "/index.theme"
    )

    icon_themes = check_dir_for_icon_theme(
        icon_themes,
        _HOME + "/.icons/",
        "/index.theme"
    )

    icon_themes = check_dir_for_icon_theme(
        icon_themes,
        _HOME + "/.local/share/icons/",
        "/index.theme"
    )

    return icon_themes


def get_cursor_themes():
    cursor_themes = []

    cursor_themes = check_dir_for_file_to_list(
        cursor_themes,
        "/usr/share/icons/",
        "/cursors/"
    )
    cursor_themes = check_dir_for_file_to_list(
        cursor_themes,
        _HOME + "/.icons/",
        "/cursors/"
    )
    cursor_themes = check_dir_for_file_to_list(
        cursor_themes,
        _HOME + "/.local/share/icons/",
        "/cursors/"
    )

    return cursor_themes

#
# def get_extensions():
#     extensions = []
#
#     extensions = check_dir_for_file_to_list(
#         extensions,
#         _HOME + "/.local/share/gnome-shell/extensions/",
#         "/extension.js"
#     )
#     extensions = check_dir_for_file_to_list(
#         extensions,
#         "/usr/share/gnome-shell/extensions/",
#         "/extension.js"
#     )
#
#     return extensions
#
#
# def get_local_extension_dirs():
#     extensions = []
#
#     if os.path.isdir(_HOME + "/.local/share/gnome-shell/extensions"):
#         for item in os.listdir(_HOME + "/.local/share/gnome-shell/extensions"):
#             if item not in extensions and os.path.isdir(_HOME + "/.local/share/gnome-shell/extensions/" + item) \
#                     and os.path.exists(_HOME + "/.local/share/gnome-shell/extensions/" + item + "/metadata.json"):
#                 extensions.append(_HOME + "/.local/share/gnome-shell/extensions/" + item)
#
#     return extensions
#
#
# def get_system_extension_dirs():
#     extensions = []
#
#     if os.path.isdir("/usr/share/gnome-shell/extensions/"):
#         for item in os.listdir("/usr/share/gnome-shell/extensions/"):
#             if item not in extensions and os.path.isdir("/usr/share/gnome-shell/extensions/" + item) \
#                     and os.path.exists("/usr/share/gnome-shell/extensions/" + item + "/extension.js"):
#                 extensions.append("/usr/share/gnome-shell/extensions/" + item)
#
#     return extensions
#
#
# def get_local_extensions():
#     extensions = []
#     extensions = check_dir_for_file_to_list(
#         extensions,
#         _HOME + "/.local/share/gnome-shell/extensions/",
#         "/extension.js"
#     )
#     return extensions

functions = {
    "gtk-themes": get_gtk_themes(),
    "icon-themes": get_icon_themes(),
    "cursor-themes": get_cursor_themes()
}

# Proxy needed by extensions.
# Some of the code is stolen from GNOME Tweaks (Thank you)
class ExtensionProxy:
    def __init__(self):
        self.proxy = Gio.DBusProxy.new_sync(
            Gio.bus_get_sync(Gio.BusType.SESSION, None),
            0, None,
            'org.gnome.Shell',
            '/org/gnome/Shell',
            'org.gnome.Shell.Extensions',
            None
        )
        self.extensions = self.proxy.ListExtensions()

    def remove_extension(self, uuid):
        return self.proxy.UninstallExtension('(s)', uuid)

    def refresh(self):
        self.__init__()
