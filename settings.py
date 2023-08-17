import threading
import json
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.behaviors import CoverBehavior  # not use in this file but use in the kv file, do not remove this line
from kivy.uix.widget import Widget
from app_translator import AppTranslator
from app_translator import AppTranslator

Builder.load_file("settings.kv")


class WidgetFlagWithCheckBox(Widget):
    image_source = StringProperty("")
    check_box_language = ObjectProperty(None)
    language_name = StringProperty("")
    list_check_box = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_language, 4)

    def on_check_box_language(self, *args):
        self.list_check_box.append(self.check_box_language)
        # self.check_box_language.bind(active=self.set_language)

    def init_language(self, dt):
        current_language = AppTranslator.get_current_language()
        print(current_language)
        for i in self.list_check_box:
            if i.name == current_language:
                i.active = True


    def set_language(self, widget):
        current_lang = AppTranslator.get_current_language()
        if widget.active:
            current_lang = widget.name
            AppTranslator.set_current_language(current_lang)
            print(current_lang)
            checks_box = self.list_check_box
            self.list_check_box = []
            for i in checks_box:
                if i.name != current_lang:
                    i.active = False
                self.list_check_box.append(i)
        elif widget.name == current_lang and not widget.active:
            widget.active = True








class SettingsLayout(BoxLayout):
    text_label_language = StringProperty("Select a language")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(rgba=(0, 0, 0, 0.3))
            self.overlay = Rectangle(pos=self.pos)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()

    def language(self):
        language = AppTranslator.get_current_language()
        self.text_label_language = AppTranslator().translate_text("Select a language", language)

    def on_size(self, *args):
        self.overlay.size = self.size

    def res(self):
        self.App.get_running_app().restart()
