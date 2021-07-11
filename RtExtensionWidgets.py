import json
import os
import shutil
import subprocess
import gi

import RtUtils
import RtBaseWidgets

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, Pango

class ExtensionTopItem(RtBaseWidgets.Option):
    def __init__(self, extensioninfo, revealer, extensiondir):
        RtBaseWidgets.Option.__init__(self, extensioninfo["name"])
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
        self.extension = extensioninfo["uuid"]
        self.extension_list = self.setting.get_strv("enabled-extensions")

        if os.path.isfile(extensiondir + "/prefs.js"):
            self.settings_button = Gtk.Button()
            self.settings_button.set_image(Gtk.Image.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.BUTTON))
            self.settings_button.set_relief(Gtk.ReliefStyle.NONE)
            self.settings_button.get_style_context().add_class("circular")
            self.settings_button.set_margin_end(10)
            self.settings_button.connect("clicked", self.open_extension_settings)
            self.add(self.settings_button)

        self.switch = Gtk.Switch()
        self.switch.set_margin_bottom(5)
        self.switch.set_margin_top(5)
        self.switch.set_margin_end(10)
        self.switch.set_state(self.extension in self.extension_list)
        self.add(self.switch)

        self.reveal_button = Gtk.Button()
        self.reveal_button.set_image(Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON))
        self.reveal_button.set_relief(Gtk.ReliefStyle.NONE)
        self.reveal_button.get_style_context().add_class("circular")
        self.reveal_button.set_margin_end(10)
        self.reveal_button.connect("clicked", self.reveal_button_clicked, revealer)
        self.add(self.reveal_button)

        self.switch.connect("state-set", self.state_set)
        self.setting.connect("changed", self.setting_changed)

    def open_extension_settings(self, button):
        subprocess.run(["/usr/bin/gnome-extensions", "prefs", self.extension])

    def reveal_button_clicked(self, button, revealer):
        revealer.set_reveal_child(not revealer.get_reveal_child())
        if revealer.get_reveal_child():
            button.get_style_context().add_class("expanded")
            button.set_image(Gtk.Image.new_from_icon_name("pan-down-symbolic", Gtk.IconSize.BUTTON))
        else:
            button.get_style_context().remove_class("expanded")
            button.set_image(Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON))

    def state_set(self, switch, state):
        self.extension_list = self.setting.get_strv("enabled-extensions")
        if state is True and self.extension not in self.extension_list:
            self.extension_list.append(self.extension)
        elif state is False and self.extension in self.extension_list:
            self.extension_list.remove(self.extension)
        self.setting.set_strv("enabled-extensions", self.extension_list)

    def setting_changed(self, setting, key):
        if key == "enabled-extensions":
            self.extension_list = self.setting.get_strv("enabled-extensions")
            if self.extension in self.extension_list:
                self.switch.set_state(True)
            else:
                self.switch.set_state(False)


class ExtensionBottomItem(RtBaseWidgets.Option):
    def __init__(self, extension_info, extensiondir, removable):
        self.setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
        Gtk.Box.__init__(self, extension_info, orientation=Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        self.set_spacing(7)
        self.extension_info = extension_info
        self.set_margin_bottom(10)

        if "description" in self.extension_info:
            self.description = Gtk.Label(xalign=0)
            self.description.set_margin_start(15)
            self.description.set_margin_end(15)
            self.description.set_margin_bottom(3)
            # self.description.set_margin_top(0)
            self.description.set_ellipsize(Pango.EllipsizeMode.END)
            self.description.set_markup(
                "Description: <b>" +
                str(self.extension_info["description"]).replace("\n", " ")
                + "</b>"
            )
            self.add(self.description)

        if "version" in self.extension_info:
            self.label = Gtk.Label(xalign=0)
            self.label.set_margin_start(15)
            # self.label.set_margin_bottom(3)
            self.label.set_markup("Version: <b>" + str(self.extension_info["version"]) + "</b>")
            self.add(self.label)
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        if "url" in self.extension_info and self.extension_info["url"] != "":
            self.url_button = Gtk.Button(label="Visit Website")
            # self.url_button.set_valign(Gtk.Align.START)
            self.url_button.connect("clicked", self.launch_website)
            self.url_button.set_margin_start(15)
            self.button_box.add(self.url_button)

        if removable is True:
            self.remove_button = Gtk.Button(label="Remove")
            self.remove_button.get_style_context().add_class("destructive-action")
            # self.remove_button.set_valign(Gtk.Align.END)
            self.remove_button.set_margin_start(10)
            self.remove_button.connect("clicked", self.remove_extension, extensiondir)
            self.button_box.add(self.remove_button)
        if self.button_box.get_children() == []:
            self.button_box.destroy()
        else:
            self.add(self.button_box)

    def launch_website(self, button):
        print(None, self.extension_info["url"], Gdk.CURRENT_TIME)
        Gtk.show_uri_on_window(None, self.extension_info["url"], Gdk.CURRENT_TIME)

    def remove_extension(self, button, extensiondir):
        extension_list = self.setting.get_strv("enabled-extensions")
        if self.extension_info["uuid"] in extension_list:
            extension_list.remove(self.extension_info["uuid"])
            self.setting.set_strv("enabled-extensions", extension_list)

        shutil.rmtree(extensiondir)
        self.props.parent.destroy()
        self.destroy()


class ExtensionItem(Gtk.Box):
    def __init__(self, extension_info, dir, removable):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.bottom_box.add(ExtensionBottomItem(extension_info, dir, removable))

        self.revealer = Gtk.Revealer()
        self.revealer.add(self.bottom_box)
        self.revealer.set_reveal_child(False)

        self.top_box.add(ExtensionTopItem(extension_info, self.revealer, dir))
        self.add(self.top_box)
        self.add(self.revealer)


class ExtensionsList(Gtk.Box):
    def __init__(self, extension_dirs, removable):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        for item in extension_dirs:
            self.add(ExtensionItem(json.load(open(item + "/metadata.json")), item, removable))
            self.add(Gtk.Separator())

class ExtensionsPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.topframe = RtBaseWidgets.Frame(None)
        self.systemframe = RtBaseWidgets.Frame("Built-In Extensions")
        self.localframe = RtBaseWidgets.Frame("Manually Installed Extensions")

        print(RtUtils.get_system_extension_dirs())
        print(RtUtils.get_local_extension_dirs())

        self.systemframe.add(ExtensionsList(RtUtils.get_system_extension_dirs(), False))
        self.localframe.add(ExtensionsList(RtUtils.get_local_extension_dirs(), True))

        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.add(self.systemframe.label)
        self.add(self.systemframe)
        self.add(self.localframe.label)
        self.add(self.localframe)