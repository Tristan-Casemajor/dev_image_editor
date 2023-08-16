from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.behaviors import CoverBehavior  # not use in this file but use in the kv file, do not remove this line
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.widget import Widget

Builder.load_file("settings.kv")


class WidgetFlagWithCheckBox(Widget):
    image_source = StringProperty("")
    check_box_language = ObjectProperty(None)
    language_name = StringProperty("")
    list_check_box = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_check_box_language(self, *args):
        self.list_check_box.append(self.check_box_language)
        # self.check_box_language.bind(active=self.set_language)

    def set_language(self, widget):
        if widget.active:
            current_lang = widget.name
            print(current_lang)
            checks_box = self.list_check_box
            self.list_check_box = []
            for i in checks_box:
                if i.name != current_lang:
                    i.active = False
                elif i.name == current_lang:
                    i.active = True
                self.list_check_box.append(i)






class SettingsLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(rgba=(0, 0, 0, 0.3))
            self.overlay = Rectangle(pos=self.pos)

    def on_size(self, *args):
        self.overlay.size = self.size
