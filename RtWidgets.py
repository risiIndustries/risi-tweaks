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

        if text is not None and text != "" and text.lower() != "none":
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


class ExtensionToggle(Toggle):
    def __init__(self, label, extension):
        Toggle.__init__(self, label)
        self.setting = known_schemas["org.gnome.shell"]
        self.extension = extension
        self.extensionlist = self.setting.get_strv("enabled-extensions")

        self.switch.set_state(extension in self.extensionlist)

        self.switch.connect("state-set", self.state_set)
        self.setting.connect("changed", self.setting_changed)

    def state_set(self, switch, state):
        self.extensionlist = self.setting.get_strv("enabled-extensions")
        if state is True and self.extension not in self.extensionlist:
            self.extensionlist.append(self.extension)
        elif state is False and self.extension in self.extensionlist:
            self.extensionlist.remove(self.extension)
        self.setting.set_strv("enabled-extensions", self.extensionlist)

    def setting_changed(self, setting, key):
        if key == "enabled-extensions":
            self.extensionlist = self.setting.get_strv("enabled-extensions")
            if self.extension in self.extensionlist:
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

        for entry in self.menu:
            self.dropdown.append_text(entry)
        if type(self.case) == list:
            for count, item in enumerate(self.case):
                if item == self.case[count]:
                    if not self.setting.get_string(key) in self.case:
                        self.dropdown.append_text(self.setting.get_string(key))
                        self.menu.append(self.setting.get_string(key))
                        self.case.append(self.setting.get_string(key))

                    self.dropdown.set_active(
                        self.case.index(self.setting.get_string(key))
                    )
        elif self.case == "lower":
            self.case = []
            for item in self.menu:
                self.case.append(item.lower())

            if self.setting.get_string(key).lower() not in self.case:
                self.dropdown.append_text(self.setting.get_string(key).capitalize())
                self.menu.append(self.setting.get_string(key).capitalize())
                self.case.append(self.setting.get_string(key).capitalize())

            self.dropdown.set_active(
                self.case.index(self.setting.get_string(key).lower())
            )

        elif self.case == "same":
            self.case = self.menu
            if self.setting.get_string(key) not in self.case:
                self.dropdown.append_text(self.setting.get_string(key))
                self.menu.append(self.setting.get_string(key))
                self.case.append(self.setting.get_string(key))

            self.dropdown.set_active(
                self.case.index(self.setting.get_string(key))
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
                        self.dropdown.set_active(self.case[new_value].capitalize())
                    else:
                        self.dropdown.set_active(self.case[new_value])
                except KeyError:
                    print("KeyError")
                    if type(self.case) == list and self.new_value not in self.case:
                        self.case.append(new_value)
                    self.dropdown.append_text(new_value)
                    self.menu.append(self.setting.get_string(key))
                    self.case.append(self.setting.get_string(key))
                    self.dropdown.set_active(self.dropdownindex[new_value])
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
            self, text, schema, key, value_type,
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
        self.value_type = value_type

        if self.value_type == "int":
            self.value = self.setting.get_int(key)
        elif self.value_type == "uint":
            self.value = self.setting.get_uint(key)
        elif self.value_type == "double":
            self.value = self.setting.get_double(key)

        if self.percent is True:
            self.value *= 100
        self.spin_button.set_value(self.value)


        self.spin_button.connect("value-changed", self.value_changed, key)
        self.setting.connect("changed", self.changed, key)

    def value_changed(self, spinbutton, key):
        self.value = self.spin_button.get_value()
        if self.percent is True:
            self.value *= 100

        if self.value_type == "int":
            self.setting.set_int(key, self.value)
        elif self.value_type == "uint":
            self.setting.set_uint(key, self.value)
        elif self.value_type == "double":
            self.setting.set_double(key, self.value)

    def changed(self, setting, key0, key1):
        if key0 == key1:
            if self.setting.get_double(key0) != self.spin_button.get_value():
                if self.percent is False:
                    self.spin_button.set_value(self.setting.get_double(key0))
                elif self.percent is True:
                    self.spin_button.set_value(
                        self.setting.get_double(key0) * 100
                    )


requires_extension = []
def check_for_dependent_extensions():
    extensions = RtUtils.get_extensions()
    for widget in requires_extension:
        widget.set_visible(widget.required_extension in extensions)


def setting_to_widget(widget):
    try:
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
                widget["spinbutton_value_type"],
                widget["spinbutton_min"],
                widget["spinbutton_max"],
                widget["spinbutton_step"],
                widget["stepbutton_percentage"]
            )
        elif widget["type"] == "ExtensionToggle":
            extension_required_widget = ExtensionToggle(
                widget["name"],
                widget["extension"]
            )
            extension_required_widget.required_extension = widget["extension"]
            requires_extension.append(extension_required_widget)
            return extension_required_widget
        else:
            print(widget)
            return Label("Error")
    except KeyError as e:
        print(widget)
        return Label("Error")