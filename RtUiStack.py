# The UI Stack that contains other pages
# Window -> UI
# Licensed Under LGPL3
# By PizzaLovingNerd

import gi
from RtAppearance import RtAppearance
from RtLayout import RtLayout

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RtUiStack(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        self.sidebar = Gtk.StackSidebar()
        self.stack = Gtk.Stack()
        self.sidebar.set_stack(self.stack)

        self.stack.add_titled(RtAppearance(), "appearance", "Appearance")
        self.stack.add_titled(RtLayout(), "layout", "Layout")

        self.add(self.sidebar)
        self.add(self.stack)
