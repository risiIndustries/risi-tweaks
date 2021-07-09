# All of the custom widgets we might need for risiTweaks are in this file.
# Licensed Under LGPL3
# By PizzaLovingNerd

import os
import gi

import RtUtils

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

_HOME = os.getenv("HOME")
_EXTENSIONS = "{0}/.local/share/gnome-shell/extensions/".format(_HOME)

# For code optimization by avoiding duplicate classes
known_schemas = {"org.gnome.shell": Gio.Settings.new("org.gnome.shell")}

# Frame Container (Thanks PizzaMartijn)
class Frame(Gtk.Frame):
    def __init__(self, text):
        Gtk.Frame.__init__(self)
        self.framebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.get_style_context().add_class('view')
        self.set_margin_bottom(16)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        if text is not None or text != "":
            self.label = Gtk.Label(label=text, xalign=0.0)
            self.label.get_style_context().add_class('heading')
            self.label.set_margin_bottom(8)

        Gtk.Frame.add(self, self.box)

    def add(self, *args):
        self.box.add(*args)


# Generic Option
class Option(Gtk.Box):
    def __init__(self, text):
        Gtk.Box.__init__(self)
        self.label = Gtk.Label(label=text)
        self.label.set_xalign(0)
        self.label.set_margin_start(15)
        self.label.set_margin_end(30)
        self.label.set_hexpand(True)
        self.add(self.label)

# Label and Description Options
class Label(Option):
    def __init__(self, text):
        Option.__init__(self, text)
        self.label.set_markup("<b>" + text + "</b>")
        self.label.get_style_context().add_class('heading')
        self.label.set_margin_top(15)
        self.label.set_margin_bottom(10)

class Description(Option):
    def __init__(self, text):
        Option.__init__(self, text)
        self.label.set_markup("<small>" + text + "</small>")
        self.label.get_style_context().add_class('dim-label')
        self.label.set_margin_top(5)
        self.label.set_margin_bottom(2.5)

# Toggle Options
class Toggle(Option):
    def __init__(self, text):
        Option.__init__(self, text)
        self.switch = Gtk.Switch()
        self.switch.set_margin_bottom(5)
        self.switch.set_margin_top(5)
        self.switch.set_margin_end(15)
        self.add(self.switch)


class ToggleGSetting(Toggle):
    def __init__(self, text, schema, key):
        Toggle.__init__(self, text)
        if schema not in known_schemas:
            known_schemas[schema] = Gio.Settings.new(schema)

        self.setting = known_schemas[schema]

        self.switch.set_state(self.setting.get_boolean(key))
        self.switch.connect("state-set", self.state_set, key)
        self.setting.connect("changed", self.setting_changed, key)

    def state_set(self, switch, state, key):
        self.setting.set_boolean(key, state)

    def setting_changed(self, setting, changed_key, key):
        if changed_key == key:
            new_value = self.setting.get_boolean(key)
            old_value = self.switch.get_state()
            if new_value != old_value:
                self.switch.set_state(new_value)


class ExtensionToggleSetting(Toggle):
    def __init__(self, text, key, extension, directory):
        Toggle.__init__(self, text)
        self.extension = "org.gnome.shell.extensions." + extension
        self.setting_lookup = Gio.SettingsSchemaSource.get_default()
        if self.setting_lookup.lookup(self.extension, True) is None:
            self.setting_lookup = Gio.SettingsSchemaSource.new_from_directory(
                _EXTENSIONS + directory + "/schemas/",
                None, False
            )
            self.setting = Gio.Settings.new_full(
                self.settinglookup.lookup(
                    self.extension,
                    True
                ),
                None, None)

        self.switch.set_state(self.setting.get_boolean(key))

        self.switch.connect("state-set", self.state_set, key)
        self.setting.connect("changed", self.setting_changed, key)

    def state_set(self, switch, state, key):
        self.setting.set_boolean(key, state)

    def setting_changed(self, setting, changed_key, key):
        if changed_key == key:
            new_value = self.setting.get_boolean(key)
            old_value = self.switch.get_state()
            if self.new_value != self.old_value:
                self.switch.set_state(self.new_value)


class ExtensionToggle(Toggle):
    def __init__(self, label, extension):
        Toggle.__init__(self)
        self.settings = known_schemas["org.gnome.shell"]
        self.extensionlist = self.settings.get_strv("enabled-extensions")

        if extension in self.list:
            self.switch.set_state(True)
        else:
            self.switch.set_state(False)

        self.switch.connect("state-set", self.state_set, extension)
        self.setting.connect("changed", self.setting_changed, extension)

        def state_set(self, switch, state, extension):
            if state is True and extension not in self.list:
                self.list.append(extension)
            elif state is False and extension in self.list:
                self.list.remove(extension)
            self.setting.set_strv("enabled-extensions", self.list)

        def setting_changed(self, setting, key, extension):
            if key == "enabled-extensions":
                self.list = self.setting.get_strv("enabled-extensions")
                if extension in self.list:
                    self.switch.set_state(True)
                else:
                    self.switch.set_state(False)


# Dropdown Options
class Dropdown(Option):
    def __init__(self, text):
        Option.__init__(self, text)
        self.dropdown = Gtk.ComboBoxText()
        self.dropdown.set_margin_bottom(2.5)
        self.dropdown.set_margin_top(2.5)
        self.dropdown.set_margin_end(15)
        self.add(self.dropdown)


class DropdownGSetting(Dropdown):
    def __init__(self, text, schema, key, menu, case):
        Dropdown.__init__(self, text)
        if schema not in known_schemas:
            known_schemas[schema] = Gio.Settings.new(schema)

        self.setting = known_schemas[schema]
        if isinstance(menu, str):
            menu = RtUtils.functions[menu]

        self.menu = menu
        self.case = case

        self.dropdownindex = {}
        self.dropdownindexid = 0

        for entry in self.menu:
            self.dropdown.append_text(entry)
            self.dropdownindex[entry] = self.dropdownindexid
            self.dropdownindexid = self.dropdownindexid + 1
        if type(self.case) == list:
            for count, item in enumerate(self.case):
                if item == self.case[count]:
                    if not self.setting.get_string(key) in self.case:
                        self.dropdown.append_text(self.setting.get_string(key))
                        self.dropdownindex[self.setting.get_string(key)] = self.dropdownindexid
                        self.dropdownindexid = self.dropdownindexid + 1
                        self.menu.append(self.setting.get_string(key))
                        self.case.append(self.setting.get_string(key))

                    self.dropdown.set_active(
                        self.dropdownindex[self.menu[count]]
                    )
        elif self.case == "lower":
            if not self.setting.get_string(key).capitalize() in self.dropdownindex:
                self.dropdown.append_text(self.setting.get_string(key).capitalize())
                self.dropdownindex[self.setting.get_string(key).capitalize()] = self.dropdownindexid
                self.dropdownindexid = self.dropdownindexid + 1

            self.dropdown.set_active(
                self.dropdownindex[self.setting.get_string(key).capitalize()]
            )

        elif self.case == "same":
            if not self.setting.get_string(key) in self.dropdownindex:
                self.dropdown.append_text(self.setting.get_string(key))
                self.dropdownindex[self.setting.get_string(key)] = self.dropdownindexid
                self.dropdownindexid = self.dropdownindexid + 1

            self.dropdown.set_active(
                self.dropdownindex[self.setting.get_string(key)]
            )

        self.dropdown.connect("changed", self.dropdown_changed, key, self.case)
        self.setting.connect("changed", self.setting_changed, key)

    def dropdown_changed(self, dropdown, key, case):
        if type(self.case) == list:
            self.setting.set_string(
                key,
                self.case[dropdown.get_active()]
            )
        elif self.case == "lower":
            self.setting.set_string(key, dropdown.get_active_text().lower())
        elif self.case == "same":
            self.setting.set_string(key, dropdown.get_active_text())


    def setting_changed(self, setting, changed_key, key):
        if changed_key == key:
            new_value = self.setting.get_string(key)
            if self.case == "lower":
                old_value = self.dropdown.get_active_text().capitalize()
            else:
                old_value = self.dropdown.get_active_text()

            if new_value != old_value:
                try:
                    if type(self.case) == list:
                        self.dropdown.set_active(self.case.index(new_value))
                    elif self.case == "lower":
                        self.dropdown.set_active(self.dropdownindex[new_value.capitalize()])
                    else:
                        self.dropdown.set_active(self.dropdownindex[new_value])
                except KeyError:
                    if type(self.case) == list and self.new_value not in self.case:
                        self.case.append(new_value)
                    self.dropdown.append_text(new_value)
                    self.dropdownindex[new_value] = self.dropdownindexid
                    self.dropdown.set_active(self.dropdownindex[new_value])
                    self.dropdownindexid = self.dropdownindexid + 1
                    self.dropdown.append_text(self.setting.get_string(key))


# Font Options
class Font(Option):
    def __init__(self, text):
        Option.__init__(self, text)
        self.font_button = Gtk.FontButton()
        self.font_button.set_margin_bottom(2.5)
        self.font_button.set_margin_top(2.5)
        self.font_button.set_margin_end(15)
        self.add(self.font_button)


class FontGSetting(Font):
    def __init__(self, text, schema, key):
        Font.__init__(self, text)

        if schema not in known_schemas:
            known_schemas[schema] = Gio.Settings.new(schema)

        self.setting = known_schemas[schema]

        self.font_button.set_font(self.setting.get_string(key))
        self.font_button.connect("font-set", self.font_changed, key)
        self.setting.connect("changed", self.key_changed, key)

    def font_changed(self, font_button, key):
        self.setting.set_string(key, self.font_button.get_font())

    def key_changed(self, setting, key0, key1):
        if key0 == key1:
            new_value = self.setting.get_string(key0)
            old_value = self.font_button.get_font()
            if new_value != old_value:
                self.font_button.set_font(self.setting.get_string(key0))


# SpinButton
class SpinButton(Option):
    def __init__(self, text, minint, maxint, step):
        Option.__init__(self, text)
        self.spin_button = Gtk.SpinButton.new_with_range(
            minint, maxint, step
        )
        self.spin_button.set_margin_bottom(2.5)
        self.spin_button.set_margin_top(2.5)
        self.spin_button.set_margin_end(15)
        self.add(self.spin_button)


class SpinButtonGSetting(SpinButton):
    def __init__(
            self, text, schema, key,
            minint, maxint, step, percent
    ):
        if percent:
            SpinButton.__init__(self, text, minint * 100, maxint * 100, step * 100)
        else:
            SpinButton.__init__(self, text, minint, maxint, step)

        if schema not in known_schemas:
            known_schemas[schema] = Gio.Settings.new(schema)

        self.setting = known_schemas[schema]

        self.percent = percent
        if self.percent is False:
            self.spin_button.set_value(self.setting.get_double(key))

        elif self.percent is True:
            self.spin_button.set_value(self.setting.get_double(key) * 100)

        self.spin_button.connect("value-changed", self.value_changed, key)
        self.setting.connect("changed", self.changed, key)

    def value_changed(self, spinbutton, key):
        if self.percent is False:
            self.setting.set_double(key, self.spin_button.get_value())
        elif self.percent is True:
            self.setting.set_double(key, self.spin_button.get_value() / 100)

    def changed(self, setting, key0, key1):
        if key0 == key1:
            if self.setting.get_double(key0) != self.spin_button.get_value():
                if self.percent is False:
                    self.spin_button.set_value(self.setting.get_double(key0))
                elif self.percent is True:
                    self.spin_button.set_value(
                        self.setting.get_double(key0) * 100
                    )


def setting_to_widget(widget):
    if widget["type"] == "ToggleGSetting":
        return ToggleGSetting(
            widget["name"],
            widget["gsetting_schema"],
            widget["gsetting_key"]
        )

    elif widget["type"] == "DropdownGSetting":
        return DropdownGSetting(
            widget["name"],
            widget["gsetting_schema"],
            widget["gsetting_key"],
            widget["dropdown_options"],
            widget["dropdown_keys"]
        )
    elif widget["type"] == "FontGSetting":
        return FontGSetting(
            widget["name"],
            widget["gsetting_schema"],
            widget["gsetting_key"]
        )
    elif widget["type"] == "SpinButtonGSetting":
        return SpinButtonGSetting(
            widget["name"],
            widget["gsetting_schema"],
            widget["gsetting_key"],
            widget["spinbutton_min"],
            widget["spinbutton_max"],
            widget["spinbutton_step"],
            True
        )
    else:
        raise ValueError("You suck at coding")