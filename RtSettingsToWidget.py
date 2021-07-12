import RtBaseWidgets
import RtCustomWidgets
import RtUtils
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

needs_start_function = []
requires_extension = []
known_schemas = RtBaseWidgets.known_schemas


def setting_to_widget(setting):
    if "description" in setting:
        widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        widget.add(get_base_widget(setting))
        widget.add(RtBaseWidgets.Description(setting["description"]))
    else:
        widget = get_base_widget(setting)

    if "requires_extension" in setting:
        widget.requires_extension = setting["requires_extension"]
        requires_extension.append(widget)

    return widget


def get_base_widget(widget):
    if "type" in widget:
        if widget["type"] == "ToggleGSetting":
            return RtBaseWidgets.ToggleGSetting(
                widget["name"],
                widget["gsetting"][0],
                widget["gsetting"][1]
            )
        elif widget["type"] == "DropdownGSetting":
            return RtBaseWidgets.DropdownGSetting(
                widget["name"],
                widget["gsetting"][0],
                widget["gsetting"][1],
                widget["dropdown_options"],
                widget["dropdown_keys"]
            )
        elif widget["type"] == "FontGSetting":
            return RtBaseWidgets.FontGSetting(
                widget["name"],
                widget["gsetting"][0],
                widget["gsetting"][1]
            )
        elif widget["type"] == "SpinButtonGSetting":
            return RtBaseWidgets.SpinButtonGSetting(
                widget["name"],
                widget["gsetting"][0],
                widget["gsetting"][1],
                widget["spinbutton_value_type"],
                widget["spinbutton_min"],
                widget["spinbutton_max"],
                widget["spinbutton_step"],
                widget["stepbutton_percentage"]
            )
        elif widget["type"] == "ExtensionToggle":
            return RtBaseWidgets.ExtensionToggle(
                widget["name"],
                widget["extension"]
            )
        else:
            return get_custom_widget(widget)
    else:
        print(widget)
        return RtBaseWidgets.Label("Error")


def get_custom_widget(setting):
    if "type" in setting:
        if setting["type"] == "RaiseWindowWhenFocused":
            widget = RtCustomWidgets.RaiseWindowWhenFocused()
            needs_start_function.append(widget)
            return widget
        else:
            print(setting)
            return RtBaseWidgets.Label("Error")
    else:
        print(setting)
        return RtBaseWidgets.Label("Error")


def check_for_dependent_extensions():
    for widget in requires_extension:
        widget.set_visible(True)
    # extensions = RtUtils.get_extensions()
    # for widget in requires_extension:
    #     widget.set_visible(widget.requires_extension in extensions)


def run_start_functions():
    for widget in needs_start_function:
        widget.start_function()