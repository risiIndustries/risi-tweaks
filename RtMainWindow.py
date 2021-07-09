import gi
import os
import glob
import yaml
import RtWidgets

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RtMainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Risi Tweaks")

        # Creating the Header Bar and the two views for the Header Bar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.window_stack = Gtk.Stack()

        for dir in glob.glob(os.getcwd() + "/tweaks/*"):

            self.stack = Gtk.Stack()
            self.stackbox = Gtk.Box()

            for file in os.listdir(dir):
                if file.endswith(".yml") or file.endswith(".yaml"):
                    with open(dir + "/" + file) as f:
                        self.data = yaml.safe_load(f)
                        self.stackpage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                        for section in self.data:
                            self.section = section["section"]
                            self.label = self.section["name"]
                            for settings in self.section:
                                if settings == "name":
                                    continue
                                self.frame = RtWidgets.Frame(self.label)
                                for setting in self.section["settings"]:
                                    self.frame.add(RtWidgets.setting_to_widget(setting))
                                self.stackpage.set_margin_start(10)
                                self.stackpage.set_margin_end(10)
                                self.stackpage.set_margin_top(10)
                                self.stackpage.set_margin_bottom(10)

                                self.stackpage.add(self.frame.label)
                                self.stackpage.add(self.frame)
                self.stackpagename = os.path.basename(os.path.splitext(dir + "/" + file)[0])
                self.stack.add_titled(self.stackpage, self.stackpagename.lower().replace(" ", "_"), self.stackpagename)
            self.stackname = os.path.basename(dir)
            self.stackbox.add(Gtk.StackSidebar(stack=self.stack))
            self.stackbox.add(self.stack)
            self.window_stack.add_titled(self.stackbox, self.stackname.lower().replace(" ", "_"), self.stackname)


        # self.ui_stack = Gtk.Stack()
        # self.system_stack = Gtk.Stack()
        # self.window_stack.add_titled(RtUiStack(), "ui", "UI")
        # self.window_stack.add_titled(self.system_stack, "system", "System")

        self.stack_switcher = Gtk.StackSwitcher(stack=self.window_stack)
        self.header.set_custom_title(self.stack_switcher)
        self.set_titlebar(self.header)

        self.add(self.window_stack)
        self.show_all()
