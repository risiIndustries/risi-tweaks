# This class converts settings from a yaml file to a widget.
# Licensed under GPL3
# By PizzaLovingNerd

import RtBaseWidgets
import RtCustomWidgets
import RtAppearanceWidgets
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

needs_start_function = []
requires_extension = []
known_schemas = RtBaseWidgets.known_schemas
application = None


# Checks for special properties in a widget before returning a widget
def setting_to_widget(setting):
    if "description" in setting:  # Creates a box to add description under the widget if description is added.
        widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        widget.add(get_base_widget(setting))  # Gets the setting's needed widget from get_base_widget
        widget.add(RtBaseWidgets.Description(setting["description"]))  # Adds description
    else:
        widget = get_base_widget(setting)  # Gets the setting's needed widget from get_base_widget

    if "requires_extension" in setting:  # Checks if widget requires extension and adds it to list if it does.
        widget.requires_extension = setting["requires_extension"]
        requires_extension.append(widget)

    return widget


# Converts setting from yaml to widget
def get_base_widget(setting):
    if "type" in setting:
        if setting["type"] == "ToggleGSetting":
            return RtBaseWidgets.ToggleGSetting(
                setting["name"],
                setting["gsetting"][0],
                setting["gsetting"][1]
            )
        elif setting["type"] == "DropdownGSetting":
            return RtBaseWidgets.DropdownGSetting(
                setting["name"],
                setting["gsetting"][0],
                setting["gsetting"][1],
                setting["dropdown_options"],
                setting["dropdown_keys"]
            )
        elif setting["type"] == "FontGSetting":
            return RtBaseWidgets.FontGSetting(
                setting["name"],
                setting["gsetting"][0],
                setting["gsetting"][1]
            )
        elif setting["type"] == "SpinButtonGSetting":
            return RtBaseWidgets.SpinButtonGSetting(
                setting["name"],
                setting["gsetting"][0],
                setting["gsetting"][1],
                setting["spinbutton_value_type"],
                setting["spinbutton_min"],
                setting["spinbutton_max"],
                setting["spinbutton_step"],
                setting["stepbutton_percentage"]
            )
        elif setting["type"] == "ExtensionToggle":
            return RtBaseWidgets.ExtensionToggle(
                setting["name"],
                setting["extension"]
            )
        else:
            return get_custom_widget(setting)  # Tries to get a custom widget if it's not a base widget
    else:
        print(setting)
        return RtBaseWidgets.Label("Error")


# Same as get_base_widget but for custom widgets
def get_custom_widget(setting):
    if "type" in setting:
        if setting["type"] == "RaiseWindowWhenFocused":
            widget = RtCustomWidgets.RaiseWindowWhenFocused()
            needs_start_function.append(widget)
            return widget
        if setting["type"] == "AccentColors":
            widget = RtAppearanceWidgets.AccentColors()
            return widget
        if setting["type"] == "CustomColorsButton":
            widget = RtAppearanceWidgets.CustomColorsButton(application)
            return widget
        else:
            print(f"Error involving: {str(setting)}")
            return RtBaseWidgets.Label("Error")
    else:
        print(f"Error involving: {str(setting)}")
        return RtBaseWidgets.Label("Error")


# Sets visible for widget based on if dependent extension is installed.
def check_for_dependent_extensions():
    setting = RtBaseWidgets.known_schemas["org.gnome.shell"]
    extensions = setting.get_strv("enabled-extensions")
    for widget in requires_extension:
        widget.set_visible(widget.requires_extension in extensions)


# Runs extra function for widget if it needs one.
def run_start_functions():
    for widget in needs_start_function:
        widget.start_function()
