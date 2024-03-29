# Loads up main window
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import os
import glob
import yaml
import RtBaseWidgets
import RtExtensionWidgets
import RtRisiScript
import RtSettingsToWidget
import RtExperimentsWidgets
import pathlib

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# Launches main window of risiTweaks
class RtMainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="risiTweaks")
        RtSettingsToWidget.application = app
        self.set_default_size(-1, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("io.risi.tweaks")

        # Creating the Header Bar and the two views for the Header Bar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.window_stack = Gtk.Stack()

        # Finds every dir where yaml files could be stored
        for dir in glob.glob(str(pathlib.Path(__file__).parent.resolve()) + "/tweaks/*"):

            self.stack = Gtk.Stack()
            self.stackbox = Gtk.Box()

            # Runs code for every yaml file
            for file in sorted(os.listdir(dir)):
                if file.endswith(".yml") or file.endswith(".yaml"):
                    with open(dir + "/" + file) as f:
                        self.data = yaml.safe_load(f)  # Loads yaml file as dictionary
                        self.stack_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                        for section in self.data:
                            self.section = section["section"]  # Gets section of yaml file
                            self.label = self.section["name"]
                            for settings in self.section:
                                if settings == "name":
                                    continue
                                self.frame = RtBaseWidgets.Frame(self.label)  # Creates frame for section in YAML file
                                for setting in self.section["settings"]:  # Creates a widget from yaml file setting
                                    self.frame.add(RtSettingsToWidget.setting_to_widget(setting))
                                self.stack_page.set_margin_start(10)
                                self.stack_page.set_margin_end(10)
                                self.stack_page.set_margin_top(10)
                                self.stack_page.set_margin_bottom(10)
                                if self.label is not None and self.label != "" and self.label.lower() != "none":
                                    self.stack_page.add(self.frame.label)  # Adds label if it exists
                                self.stack_page.add(self.frame)  # Adds frame
                                self.scrolled_page = Gtk.ScrolledWindow()  # Creates page in scrolled window
                                self.scrolled_page.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
                                self.scrolled_page.add(self.stack_page)
                self.stackpagename = os.path.basename(os.path.splitext(dir + "/" + file)[0])  # Creates name for stack

                # Adds page to side bar in the category
                self.stack.add_titled(
                    self.scrolled_page,
                    self.stackpagename.lower().replace(" ", "_"),
                    self.stackpagename
                )

            # Adds category to the main window's stack
            self.stackname = os.path.basename(dir)
            self.stackbox.add(Gtk.StackSidebar(stack=self.stack))
            self.stackbox.add(self.stack)
            self.window_stack.add_titled(self.stackbox, self.stackname.lower().replace(" ", "_"), self.stackname)

        # Adds extensions catagory to the main windows stack
        self.extension_scroll = Gtk.ScrolledWindow()
        self.extension_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.extension_scroll.add(RtExtensionWidgets.ExtensionsPage())
        self.window_stack.add_titled(self.extension_scroll, "extensions", "Extensions")

        # Adds risi script category to the main windows stack
        self.risiscript_scroll = Gtk.ScrolledWindow()
        self.risiscript_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.risiscript_scroll.add(RtRisiScript.RisiScriptPage())
        self.window_stack.add_titled(self.risiscript_scroll, "risiscript", "risiScript")

        # Adds experiments to the main windows stack
        self.experiments_scroll = Gtk.ScrolledWindow()
        self.experiments_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.experiments_scroll.add(RtExperimentsWidgets.RisiExperimentsPage())
        self.window_stack.add_titled(self.experiments_scroll, "experiments", "Experiments")

        # Adds catagory stack pages to title bar
        self.stack_switcher = Gtk.StackSwitcher(stack=self.window_stack)
        self.header.set_custom_title(self.stack_switcher)
        self.set_titlebar(self.header)

        self.add(self.window_stack)

        self.show_all()

        RtSettingsToWidget.check_for_dependent_extensions()
        RtSettingsToWidget.run_start_functions()
