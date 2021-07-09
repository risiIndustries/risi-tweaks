# Main file, loads up main window
# Licensed Under LGPL3
# By PizzaLovingNerd

import gi
from RtMainWindow import RtMainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == '__main__':
    window = RtMainWindow()
    window.connect("delete-event", Gtk.main_quit)
    Gtk.main()
