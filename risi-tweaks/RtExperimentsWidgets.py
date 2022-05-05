import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RisiExperimentsPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        label = Gtk.Label()
        label.set_markup(
            "<big><b>risiExperiments</b></big>\n"
            "<b>Coming Soon</b>\n\n"
            "This page will be used for enabling new experimental features that are still in the testing phase."
        )
        label.set_justify(Gtk.Justification.CENTER)
        label.set_vexpand(True)
        label.set_hexpand(True)
        self.add(label)
