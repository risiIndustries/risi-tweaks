# Main file, loads up main window class
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
from RtMainWindow import RtMainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="io.risi.Tweaks"
        )
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = RtMainWindow(self)
            self.window.set_title("risiTweaks")
            self.window.set_icon_name("webapp-manager")
            self.add_window(self.window)
            self.window.show_all()
        self.window.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = Application()
    app.run()
