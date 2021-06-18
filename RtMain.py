# Main file, loads up main window
# Licensed Under LGPL3
# By PizzaLovingNerd

import gi
from RtUiStack import RtUiStack

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Risi Tweaks")

        # Creating the Header Bar and the two views for the Header Bar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)

        self.window_stack = Gtk.Stack()
        self.ui_stack = Gtk.Stack()
        self.system_stack = Gtk.Stack()
        self.window_stack.add_titled(RtUiStack(), "ui", "UI")
        self.window_stack.add_titled(self.system_stack, "system", "System")

        self.stack_switcher = Gtk.StackSwitcher(stack=self.window_stack)
        self.header.set_custom_title(self.stack_switcher)
        self.set_titlebar(self.header)

        self.add(self.window_stack)
        self.show_all()

if __name__ == '__main__':
    window = Window()
    window.connect("delete-event", Gtk.main_quit)
    Gtk.main()
