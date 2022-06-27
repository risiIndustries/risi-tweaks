import os
import subprocess
import yaml

import gi
import risiscript

from enum import Enum

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class RisiScriptState(Enum):
    INSTALLED_APP = 1
    TRUSTED_INSTALLER = 2
    TRUSTED_SCRIPT = 3
    UNTRUSTED_INSTALLER = 4
    UNTRUSTED_SCRIPT = 5


class RisiScriptPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        scripts = load_risi_scripts()

        self.stack = Gtk.Stack()
        self.sidebar = RisiScriptStackSidebar(self.stack, scripts)

        self.add(self.sidebar)
        self.add(self.stack)

        self.stack.add_named(EmptyPage(), "empty")
        for script in scripts:
            self.stack.add_named(RisiScriptStackPage(script), script.metadata.id)

        self.show_all()


class RisiScriptStackSidebar(Gtk.ScrolledWindow):
    def __init__(self, stack, scripts):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.stack = stack

        self.listbox = Gtk.ListBox()
        self.listbox.get_style_context().add_class("sidebar")
        self.add(self.listbox)

        self.scripts = scripts

        self.add_apps_for_state(RisiScriptState.INSTALLED_APP, "Installed Apps:")
        self.add_apps_for_state(RisiScriptState.TRUSTED_INSTALLER, "Trusted Installers:")
        self.add_apps_for_state(RisiScriptState.TRUSTED_SCRIPT, "Trusted Scripts:")
        self.add_apps_for_state(RisiScriptState.UNTRUSTED_INSTALLER, "Untrusted Installers:")
        self.add_apps_for_state(RisiScriptState.UNTRUSTED_SCRIPT, "Untrusted Scripts:")

        self.listbox.connect("row_selected", self.row_selected)

    def add_apps_for_state(self, state, state_label):
        if self.scripts:
            scripts = [script for script in self.scripts if script.state == state]
        else:
            scripts = None

        if scripts:
            self.listbox.add(RisiScriptStateLabel(state_label))
            for script in scripts:
                self.listbox.add(RisiScriptItem(script))

    def row_selected(self, listbox, row):
        self.stack.set_visible_child_name(row.script.metadata.id)


class RisiScriptItem(Gtk.ListBoxRow):
    def __init__(self, script):
        Gtk.ListBoxRow.__init__(self)

        label = Gtk.Label(label=script.metadata.name, xalign=0)
        label.set_margin_start(10)
        label.set_margin_end(10)
        label.set_margin_top(10)
        label.set_margin_bottom(10)

        self.script = script
        self.id = self.script.metadata.id

        self.add(label)


class RisiScriptStateLabel(Gtk.ListBoxRow):
    def __init__(self, text):
        Gtk.ListBoxRow.__init__(self)

        label = Gtk.Label(label=text, xalign=0)
        label.set_markup(f"<b>{text}</b>")
        label.set_margin_start(10)
        label.set_margin_end(10)
        label.set_margin_top(10)

        self.add(label)
        self.set_selectable(False)
        self.set_activatable(False)


class RisiScriptStackPage(Gtk.Box):
    def __init__(self, script):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.script = script

        self.trusted = self.script.state in [
            RisiScriptState.INSTALLED_APP,
            RisiScriptState.TRUSTED_INSTALLER,
            RisiScriptState.TRUSTED_SCRIPT
        ]

        name = Gtk.Label(label=script.metadata.name, xalign=0)
        name.set_markup(f"<b>{script.metadata.name}</b>")
        name.set_vexpand(True)
        name.set_valign(Gtk.Align.FILL)
        name.set_margin_bottom(5)
        description = Gtk.Label(label=script.metadata.description, xalign=0)
        description.set_vexpand(True)
        description.set_valign(Gtk.Align.FILL)

        # Button
        button = Gtk.Button(label="Run Script")
        if self.script.state == RisiScriptState.INSTALLED_APP:
            button.set_label("Manage App")
        elif self.script.state in [RisiScriptState.TRUSTED_INSTALLER, RisiScriptState.UNTRUSTED_INSTALLER]:
            button.set_label("Install App")
        button.connect("clicked", self.launch_risi_script)
        button.set_hexpand(True)
        button.set_halign(Gtk.Align.END)
        button.set_valign(Gtk.Align.CENTER)
        button.get_style_context().add_class("suggested-action")

        top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        top_box.set_hexpand(True)
        top_box.set_vexpand(False)
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        text_box.add(name)
        text_box.add(description)
        top_box.add(text_box)
        top_box.add(button)
        self.add(top_box)

        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

    def launch_risi_script(self, button):
        procargs = ["risi-script-gtk", "--file", self.script.location]
        if self.trusted:
            procargs.append("--trusted")
        subprocess.Popen(procargs)


class EmptyPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        label = Gtk.Label()
        label.set_markup(
            "<big><b>risiScript</b></big>\n\n"
            "Tweak your system the easy way"
        )
        label.set_justify(Gtk.Justification.CENTER)
        label.set_vexpand(True)
        label.set_hexpand(True)
        self.add(label)


def load_risi_scripts():
    scripts = []
    if not os.path.isdir("/usr/share/risi-script/scripts"):
        try:
            os.makedirs("/usr/share/risi-script/scripts")
        except PermissionError:
            return None
    for file in os.listdir("/usr/share/risi-script/scripts"):
        if file[-7:] == ".risisc":
            with open("/usr/share/risi-script/scripts/" + file, "r") as f:
                try:
                    script = risiscript.Script(f.read())
                except yaml.YAMLError:
                    pass
                else:
                    if script.installation_mode is True:
                        if script.installed is True:
                            script.state = RisiScriptState.INSTALLED_APP
                        else:
                            script.state = RisiScriptState.TRUSTED_INSTALLER
                    else:
                        script.state = RisiScriptState.TRUSTED_SCRIPT
                    script.location = f.name
                    scripts.append(script)

    homepath = os.path.expanduser("~") + "/.risi-script/scripts"
    if not os.path.isdir(homepath):
        os.makedirs(homepath)
    for file in os.listdir(homepath):
        if file[-7:] == ".risisc":
            with open(homepath + "/" + file, "r") as f:
                try:
                    script = risiscript.Script(f.read())
                except yaml.YAMLError:
                    pass
                else:
                    if script.installation_mode is True:
                        if script.installed is True:
                            script.state = RisiScriptState.INSTALLED_APP
                        else:
                            script.state = RisiScriptState.UNTRUSTED_INSTALLER
                    else:
                        script.state = RisiScriptState.UNTRUSTED_SCRIPT
                    script.location = f.name
                    scripts.append(script)
    return scripts

