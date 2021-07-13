# This file contains all the widgets that used for the extension page
# Licensed Under GPL3
# By PizzaLovingNerd

import subprocess
import gi

import RtUtils
import RtBaseWidgets

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

extension_proxy = RtUtils.ExtensionProxy()


# This is where the extension name, settings button,
# toggle switch, reveal button, and error indicator go
class ExtensionTopItem(RtBaseWidgets.Option):
    def __init__(self, extension, revealer):
        RtBaseWidgets.Option.__init__(self, extension["name"])
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
        self.sensitive = True
        self.revealer = revealer
        self.extension = extension
        self.extension_enabled = self.setting.get_strv("enabled-extensions")

        # Checks if the extension has an error and
        # creates an indicator if it does
        # States:
        # 1 = Enabled
        # 2 = Disabled
        # 3 = Error
        # 4 = Needs update to new GNOME version
        # 5 = Downloading
        # 6 = Initialized
        if self.extension["state"] != 1 and \
            self.extension["state"] != 2 and \
            self.extension["state"] != 6:


            if self.extension["state"] == 3:
                self.indicator = Gtk.Image.new_from_icon_name("dialog-error", Gtk.IconSize.LARGE_TOOLBAR)
                self.sensitive = False

            if self.extension["state"] == 4:
                self.indicator = Gtk.Image.new_from_icon_name("dialog-error", Gtk.IconSize.LARGE_TOOLBAR)
                self.sensitive = False

            if self.extension["state"] == 5:
                self.indicator = Gtk.Image.new_from_icon_name("emblem-downloads", Gtk.IconSize.LARGE_TOOLBAR)
                self.sensitive = False

            self.indicator.set_margin_end(10)

            self.add(self.indicator)

        # Generates settings button if extension has settings
        if self.extension["hasPrefs"]:
            self.settings_button = Gtk.Button()
            self.settings_button.set_image(Gtk.Image.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.BUTTON))
            self.settings_button.set_relief(Gtk.ReliefStyle.NONE)
            self.settings_button.get_style_context().add_class("circular")
            self.settings_button.set_margin_end(10)
            self.settings_button.connect("clicked", self.open_extension_settings)
            self.settings_button.set_sensitive(self.sensitive)
            self.add(self.settings_button)

        # Extension Toggle Switch
        self.switch = Gtk.Switch()
        self.switch.set_margin_bottom(5)
        self.switch.set_margin_top(5)
        self.switch.set_margin_end(10)
        self.switch.set_sensitive(self.sensitive)
        self.switch.set_state(self.extension["uuid"] in self.extension_enabled)
        self.add(self.switch)

        # Button to reveal bottom of ExtensionItem
        self.reveal_button = Gtk.Button()
        self.reveal_button.set_image(Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON))
        self.reveal_button.set_relief(Gtk.ReliefStyle.NONE)
        self.reveal_button.get_style_context().add_class("circular")
        self.reveal_button.set_margin_end(10)
        self.reveal_button.connect("clicked", self.reveal_button_clicked)
        self.add(self.reveal_button)

        self.switch.connect("state-set", self.state_set)
        self.setting.connect("changed", self.setting_changed)

    # Opens preferences for extension
    def open_extension_settings(self, button):
        subprocess.run(["/usr/bin/gnome-extensions", "prefs", self.extension["uuid"]])

    # Toggles if bottom of ExtensionItem is revealed.
    def reveal_button_clicked(self, button):
        # self.revealer is the revealer that holds the bottom of the item
        self.revealer.set_reveal_child(not self.revealer.get_reveal_child())
        if self.revealer.get_reveal_child():
            button.get_style_context().add_class("expanded")
            button.set_image(Gtk.Image.new_from_icon_name("pan-down-symbolic", Gtk.IconSize.BUTTON))
        else:
            button.get_style_context().remove_class("expanded")
            button.set_image(Gtk.Image.new_from_icon_name("pan-end-symbolic", Gtk.IconSize.BUTTON))

    # Sets if the extension should be enabled
    def state_set(self, switch, state):
        self.extension_enabled = self.setting.get_strv("enabled-extensions")
        if state is True and self.extension["uuid"] not in self.extension_enabled:
            self.extension_enabled.append(self.extension["uuid"])
        elif state is False and self.extension["uuid"] in self.extension_enabled:
            self.extension_enabled.remove(self.extension["uuid"])
        self.setting.set_strv("enabled-extensions", self.extension_enabled)

    # Makes sure that the extension updates if someone uses
    # dconf editor, GNOME Extensions, or the extension website to toggle one on.
    def setting_changed(self, setting, key):
        if key == "enabled-extensions":
            self.extension_enabled = self.setting.get_strv("enabled-extensions")
            if self.extension["uuid"] in self.extension_enabled:
                self.switch.set_state(True)
            else:
                self.switch.set_state(False)


# The bottom of an ExtensionItem that is hidden by default.
# Shows extra info, as well as buttons to remove and the website.
class ExtensionBottomItem(RtBaseWidgets.Option):
    def __init__(self, extension):
        self.setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
        Gtk.Box.__init__(self, extension, orientation=Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        self.set_spacing(7)
        self.extension = extension
        self.set_margin_bottom(10)

        # Checks if the extension has an error and
        # shows the error message if it does.
        # States:
        # 1 = Enabled
        # 2 = Disabled
        # 3 = Error
        # 4 = Needs update to new GNOME version
        # 5 = Downloading
        # 6 = Initialized

        if self.extension["state"] == 4 or self.extension["state"] == 4 or self.extension["state"] == 5:
            self.error = Gtk.Label(xalign=0)
            self.error.set_margin_start(15)
            self.error.set_margin_end(15)
            self.error.set_ellipsize(Pango.EllipsizeMode.END)

            if self.extension["state"] == 3:
                self.error.set_markup(
                    "Error: <b>An unknown error has occurred</b>"
                )
            if self.extension["state"] == 4:
                self.error.set_markup(
                    "Error: <b>This extension is incompatible with your version of GNOME</b>"
                )

            if self.extension["state"] == 5:
                self.error.set_markup(
                    "Error: <b>This extension is currently downloading.</b>"
                )
            self.add(self.error)

        # Adds description for the extension
        if "description" in self.extension:
            self.description = Gtk.Label(xalign=0)
            self.description.set_margin_start(15)
            self.description.set_margin_end(15)
            self.description.set_ellipsize(Pango.EllipsizeMode.END)
            self.description.set_markup(
                "Description: <b>" +
                str(self.extension["description"]).replace("\n", " ")
                + "</b>"
            )
            self.add(self.description)

        # Shows author
        if "original-author" in self.extension:
            self.original_author = Gtk.Label(xalign=0)
            self.original_author.set_margin_start(15)
            self.original_author.set_margin_end(15)
            self.original_author.set_ellipsize(Pango.EllipsizeMode.END)
            self.original_author.set_markup(
                "Original Author: <b>" +
                str(self.extension["original-author"]).replace("\n", ", ")
                + "</b>"
            )
            self.add(self.original_author)

        # Shows version
        if "version" in self.extension:
            self.label = Gtk.Label(xalign=0)
            self.label.set_margin_start(15)
            self.label.set_markup("Version: <b>" + str(self.extension["version"]) + "</b>")
            self.add(self.label)
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # Visit website button
        if "url" in self.extension and self.extension["url"] != "":
            self.url_button = Gtk.Button(label="Visit Website")
            # self.url_button.set_valign(Gtk.Align.START)
            self.url_button.connect("clicked", launch_website, self.extension["url"])
            self.url_button.set_margin_start(15)
            self.button_box.add(self.url_button)

        # Checks if the extension is installed locally and
        # Adds a remove button if it isn't.
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

    # Removes extension using extension proxy and refreshes the view.
    def remove_extension(self, button):
        extension_list = self.setting.get_strv("enabled-extensions")
        if self.extension["uuid"] in extension_list:
            extension_list.remove(self.extension["uuid"])
            self.setting.set_strv("enabled-extensions", extension_list)

        extension_proxy.remove_extension(self.extension["uuid"])
        extension_proxy.refresh()
        self.props.parent.destroy()
        self.destroy()


# ExtensionItem, combines ExtensionTopItem and ExtensionBottomItem
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


# Generates a list of extensions that can be put in a frame
class ExtensionsList(Gtk.Box):
    def __init__(self, extensions, exttype):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        for item in extensions:
            if extensions[item]["type"] == exttype:
                self.add(ExtensionItem(extensions[item]))
                self.add(Gtk.Separator())


# This generates the frames the extension lists go in.
class ExtensionsFrames(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.systemframe = RtBaseWidgets.Frame("Built-In Extensions") # Frame for built-in extensions
        self.localframe = RtBaseWidgets.Frame("Manually Installed Extensions") # Frame for local extensions

        self.extensions = extension_proxy.extensions

        self.systemframe.add(ExtensionsList(self.extensions, 1))  # Adds system installed extensions to system frame
        self.localframe.add(ExtensionsList(self.extensions, 2))  # Adds locally installed extensions to system locally

        self.add(self.systemframe.label)
        self.add(self.systemframe)
        self.add(self.localframe.label)
        self.add(self.localframe)


# This is the class for the extensions page that is put inside the main window
class ExtensionsPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.top_frame = RtBaseWidgets.Frame("")
        self.disable_frame = RtBaseWidgets.Frame("")

        # Top Frame with info and buttons
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

        # Creates button box with Refresh button, restart GNOME button,
        # and a button to launch extensions.gnome.org
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button_box.set_margin_top(10)
        self.button_box.set_spacing(5)
        self.refresh_button = Gtk.Button(label="Refresh Extensions")
        self.refresh_button.connect("clicked", self.refresh_extensions)
        self.button_box.add(self.refresh_button)
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
        self.disable_frame.add(  # Add extension toggle
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

    # Refreshes extensions if an extension is enabled
    def setting_changed(self, setting, key):
        if key == "enabled-extensions":
            self.refresh_extensions(None)

    # This function refreshes extensions by deleting the extension
    # frames and reinitializing them
    def refresh_extensions(self, *args):
        self.extension_frames.destroy()
        extension_proxy.refresh()
        self.extension_frames = ExtensionsFrames()
        self.add(self.extension_frames)
        self.extension_frames.show_all()

# Button for launching websites
def launch_website(button, url):
    Gtk.show_uri_on_window(None, url, Gdk.CURRENT_TIME)