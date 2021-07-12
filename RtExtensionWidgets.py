import json
import os
import shutil
import subprocess
import gi

import RtUtils
import RtBaseWidgets

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, Pango

extension_proxy = RtUtils.ExtensionProxy()

class ExtensionTopItem(RtBaseWidgets.Option):
    def __init__(self, extension, revealer):
        RtBaseWidgets.Option.__init__(self, extension["name"])
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
        self.revealer = revealer
        self.extension = extension
        self.extension_enabled = self.setting.get_strv("enabled-extensions")

        if self.extension["state"] != 1 and \
            self.extension["state"] != 2 and \
            self.extension["state"] != 6:

            if self.extension["state"] == 3:
                self.indicator = Gtk.Image.new_from_icon_name("dialog-name", Gtk.IconSize.LARGE_TOOLBAR)
                self.indicator.set_tooltip_text("An error has occurred")

            if self.extension["state"] == 4:
                self.indicator = Gtk.Image.new_from_icon_name("software-update-available", Gtk.IconSize.LARGE_TOOLBAR)
                self.indicator.set_tooltip_text("An update is available for this extension")

            if self.extension["state"] == 5:
                self.indicator = Gtk.Image.new_from_icon_name("emblem-downloads", Gtk.IconSize.LARGE_TOOLBAR)
                self.indicator.set_tooltip_text("This extension is currently downloading")

            self.indicator.set_margin_end(10)

            self.add(self.indicator)

        if self.extension["hasPrefs"]:
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
        self.switch.set_state(self.extension["uuid"] in self.extension_enabled)
        self.add(self.switch)

        self.reveal_button = Gtk.Button()
        self.reveal_button.set_image(Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON))
        self.reveal_button.set_relief(Gtk.ReliefStyle.NONE)
        self.reveal_button.get_style_context().add_class("circular")
        self.reveal_button.set_margin_end(10)
        self.reveal_button.connect("clicked", self.reveal_button_clicked)
        self.add(self.reveal_button)

        self.switch.connect("state-set", self.state_set)
        self.setting.connect("changed", self.setting_changed)

    def open_extension_settings(self, button):
        subprocess.run(["/usr/bin/gnome-extensions", "prefs", self.extension["uuid"]])

    def reveal_button_clicked(self, button):
        self.revealer.set_reveal_child(not self.revealer.get_reveal_child())
        if self.revealer.get_reveal_child():
            button.get_style_context().add_class("expanded")
            button.set_image(Gtk.Image.new_from_icon_name("pan-down-symbolic", Gtk.IconSize.BUTTON))
        else:
            button.get_style_context().remove_class("expanded")
            button.set_image(Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON))

    def state_set(self, switch, state):
        self.extension_enabled = self.setting.get_strv("enabled-extensions")
        if state is True and self.extension["uuid"] not in self.extension_enabled:
            self.extension_enabled.append(self.extension["uuid"])
        elif state is False and self.extension["uuid"] in self.extension_enabled:
            self.extension_enabled.remove(self.extension["uuid"])
        self.setting.set_strv("enabled-extensions", self.extension_enabled)

    def setting_changed(self, setting, key):
        if key == "enabled-extensions":
            self.extension_enabled = self.setting.get_strv("enabled-extensions")
            if self.extension["uuid"] in self.extension_enabled:
                self.switch.set_state(True)
            else:
                self.switch.set_state(False)


class ExtensionBottomItem(RtBaseWidgets.Option):
    def __init__(self, extension):
        self.setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
        Gtk.Box.__init__(self, extension, orientation=Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        self.set_spacing(7)
        self.extension = extension
        self.set_margin_bottom(10)

        if "description" in self.extension:
            self.description = Gtk.Label(xalign=0)
            self.description.set_margin_start(15)
            self.description.set_margin_end(15)
            self.description.set_margin_bottom(3)
            # self.description.set_margin_top(0)
            self.description.set_ellipsize(Pango.EllipsizeMode.END)
            self.description.set_markup(
                "Description: <b>" +
                str(self.extension["description"]).replace("\n", " ")
                + "</b>"
            )
            self.add(self.description)

        if "original-author" in self.extension:
            self.original_author = Gtk.Label(xalign=0)
            self.original_author.set_margin_start(15)
            self.original_author.set_margin_end(15)
            self.original_author.set_margin_bottom(3)
            # self.description.set_margin_top(0)
            self.original_author.set_ellipsize(Pango.EllipsizeMode.END)
            self.original_author.set_markup(
                "Original Author: <b>" +
                str(self.extension["original-author"]).replace("\n", ", ")
                + "</b>"
            )
            self.add(self.original_author)

        if "version" in self.extension:
            self.label = Gtk.Label(xalign=0)
            self.label.set_margin_start(15)
            # self.label.set_margin_bottom(3)
            self.label.set_markup("Version: <b>" + str(self.extension["version"]) + "</b>")
            self.add(self.label)
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        if "url" in self.extension and self.extension["url"] != "":
            self.url_button = Gtk.Button(label="Visit Website")
            # self.url_button.set_valign(Gtk.Align.START)
            self.url_button.connect("clicked", launch_website, self.extension["url"])
            self.url_button.set_margin_start(15)
            self.button_box.add(self.url_button)

        if self.extension["type"] == 2:
            self.remove_button = Gtk.Button(label="Remove")
            self.remove_button.get_style_context().add_class("destructive-action")
            # self.remove_button.set_valign(Gtk.Align.END)
            self.remove_button.set_margin_start(10)
            self.remove_button.connect("clicked", self.remove_extension)
            self.button_box.add(self.remove_button)
        if self.button_box.get_children() == []:
            self.button_box.destroy()
        else:
            self.add(self.button_box)

    def remove_extension(self, button):
        extension_list = self.setting.get_strv("enabled-extensions")
        if self.extension["uuid"] in extension_list:
            extension_list.remove(self.extension["uuid"])
            self.setting.set_strv("enabled-extensions", extension_list)

        extension_proxy.remove_extension(self.extension["uuid"])
        extension_proxy.refresh()
        self.props.parent.destroy()
        self.destroy()


class ExtensionItem(Gtk.Box):
    def __init__(self, extension):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.bottom_box.add(ExtensionBottomItem(extension))

        self.revealer = Gtk.Revealer()
        self.revealer.add(self.bottom_box)
        self.revealer.set_reveal_child(False)

        self.top_box.add(ExtensionTopItem(extension, self.revealer))
        self.add(self.top_box)
        self.add(self.revealer)


class ExtensionsList(Gtk.Box):
    def __init__(self, extensions, exttype):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        for item in extensions:
            if extensions[item]["type"] == exttype:
                self.add(ExtensionItem(extensions[item]))
                self.add(Gtk.Separator())


class ExtensionsFrames(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.systemframe = RtBaseWidgets.Frame("Built-In Extensions")
        self.localframe = RtBaseWidgets.Frame("Manually Installed Extensions")

        self.extensions = extension_proxy.extensions

        self.systemframe.add(ExtensionsList(self.extensions, 1))
        self.localframe.add(ExtensionsList(self.extensions, 2))

        self.add(self.systemframe.label)
        self.add(self.systemframe)
        self.add(self.localframe.label)
        self.add(self.localframe)

class ExtensionsPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.top_frame = RtBaseWidgets.Frame("")
        self.disable_frame = RtBaseWidgets.Frame("")

        self.warning_label = Gtk.Label(xalign=0.5)
        self.warning_label.set_markup(
            "<b>Warning:</b>\n"
            "Extensions may cause issues including performance and security problems.\n"
            "If you experience such thing, we recommend disabling all extensions."
        )
        self.warning_label.set_justify(Gtk.Justification.CENTER)
        self.warning_label.set_line_wrap(True)
        self.warning_label.set_margin_start(10)
        self.warning_label.set_margin_top(10)

        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button_box.set_margin_top(10)
        self.button_box.set_spacing(5)
        self.refresh_button = Gtk.Button(label="Refresh Extensions")
        self.refresh_button.connect("clicked", self.refresh_extensions)
        self.button_box.add(self.refresh_button)
        self.add_from_file_button = Gtk.Button(label="Add Extension From File")
        self.add_from_file_button.connect("clicked", self.add_extension)
        self.button_box.add(self.add_from_file_button)
        self.add_from_web_button = Gtk.Button(label="Add Extension From Web")
        self.add_from_web_button.connect("clicked", launch_website, "https://extensions.gnome.org/")
        self.button_box.add(self.add_from_web_button)
        self.button_box.add(RtBaseWidgets.SubprocessButton(
            "Restart GNOME",
            ["/usr/bin/killall", "-SIGQUIT", "gnome-shell"]
        ))
        self.button_box.set_margin_bottom(10)
        self.button_box.set_halign(Gtk.Align.CENTER)

        self.top_frame.add(self.warning_label)
        self.top_frame.add(self.button_box)
        self.disable_frame.add(
            RtBaseWidgets.ToggleGSetting(
                "Disable Extensions", "org.gnome.shell", "disable-user-extensions"
            )
        )

        self.extension_frames = ExtensionsFrames()

        self.add(self.top_frame)
        self.add(self.disable_frame)
        self.add(self.extension_frames)

        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

    def add_extension(self, button):
        file = ExtensionPicker()
        sp = subprocess.Popen(["/usr/bin/gnome-extensions", "install", file.get_path()])
        self.refresh_extensions(button)


    def refresh_extensions(self, button):
        self.extension_frames.destroy()
        extension_proxy.refresh()
        self.extension_frames = ExtensionsFrames()
        self.add(self.extension_frames)
        self.extension_frames.show_all()

class ExtensionPicker(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(
            "Choose an Extension",
            self, Gtk.FileChooserAction.OPEN,
            "Cancel", Gtk.ResponseType.CANCEL,
            "OK", Gtk.ResponseType.OK
        )
        self.filter = Gtk.FileFilter()
        self.filter.add_pattern("*.shell-extension.zip")
        self.filter.add_pattern("*.zip")
        self.add_filter(self.filter)

        self.file = self.run()
        return self.file

def launch_website(button, url):
    Gtk.show_uri_on_window(None, url, Gdk.CURRENT_TIME)