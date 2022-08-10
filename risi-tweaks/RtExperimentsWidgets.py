import os
import yaml

import gi
import RtRisiScript
import risiscript

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class RisiExperimentsPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        scripts = load_experiments()

        self.stack = Gtk.Stack()
        self.sidebar = RtRisiScript.RisiScriptStackSidebar(self.stack, scripts)

        self.add(self.sidebar)
        self.add(self.stack)

        self.stack.add_named(EmptyPage(), "empty")
        for script in scripts:
            self.stack.add_named(RtRisiScript.RisiScriptStackPage(script), script.metadata.id)

        self.show_all()


class EmptyPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        label = Gtk.Label()
        label.set_markup(
            "<big><b>risiExperiments</b></big>\n\n"
            "This page is used for enabling new experimental features\nthat are still in the testing phase."
        )
        label.set_justify(Gtk.Justification.CENTER)
        label.set_vexpand(True)
        label.set_hexpand(True)
        self.add(label)


def load_experiments():
    scripts = []
    if not os.path.isdir("/usr/share/risi-script/experiments"):
        try:
            os.makedirs("/usr/share/risi-script/experiments")
        except PermissionError:
            return None
    for file in os.listdir("/usr/share/risi-script/experiments"):
        if file[-7:] == ".risisc":
            with open("/usr/share/risi-script/experiments/" + file, "r") as f:
                try:
                    script = risiscript.Script(f.read())
                except yaml.YAMLError:
                    pass
                else:
                    if script.installation_mode is True:
                        if script.installed is True:
                            script.state = RtRisiScript.RisiScriptState.INSTALLED_APP
                        else:
                            script.state = RtRisiScript.RisiScriptState.TRUSTED_INSTALLER
                    else:
                        script.state = RtRisiScript.RisiScriptState.TRUSTED_SCRIPT
                    script.location = f.name
                    scripts.append(script)
    return scripts
