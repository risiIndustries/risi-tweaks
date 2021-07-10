# This file is a place to put extra functions for risiTweaks
# so that we don't have a bunch of random functions at the
# bottom of all our classes
# Licensed Under LGPL3
# By PizzaLovingNerd

import os

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

def get_extensions():
    extensions = []

    extensions = check_dir_for_file_to_list(
        extensions,
        _HOME + "/.local/share/gnome-shell/extensions/",
        "/extension.js"
    )
    extensions = check_dir_for_file_to_list(
        extensions,
        "/usr/share/gnome-shell/extensions/",
        "/extension.js"
    )

    return extensions

functions = {
    "gtk-themes": get_gtk_themes(),
    "icon-themes": get_icon_themes(),
    "cursor-themes": get_cursor_themes()
}