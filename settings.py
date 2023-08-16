import threading
import json
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.behaviors import CoverBehavior  # not use in this file but use in the kv file, do not remove this line
from kivy.uix.widget import Widget

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
        current_language = self.get_current_language()
        print(current_language)
        for i in self.list_check_box:
            if i.name == current_language:
                i.active = True

    def set_language(self, widget):
        current_lang = self.get_current_language()
        if widget.active:
            current_lang = widget.name
            self.set_current_language(current_lang)
            print(current_lang)
            checks_box = self.list_check_box
            self.list_check_box = []
            for i in checks_box:
                if i.name != current_lang:
                    i.active = False
                #elif i.name == current_lang:
                    #print("eee")
                    #i.active = True
                self.list_check_box.append(i)
        elif widget.name == current_lang and not widget.active:
            widget.active = True

    def get_current_language(self):
        file = open("app_settings.json", "r")
        settings_str = file.read()
        file.close()
        settings_dict = json.loads(settings_str)
        language = settings_dict["language"]
        return language
        '''file = open("language.txt", "r")
        data = file.read()
        file.close()
        return data'''

    def set_current_language(self, language):
        file = open("app_settings.json", "r")
        settings_str = file.read()
        file.close()
        settings_dict = json.loads(settings_str)
        settings_dict["language"] = language
        new_settings_str = json.dumps(settings_dict)
        file = open("app_settings.json", "w")
        file.write(new_settings_str)
        file.close()

        '''file = open("language.txt", "w")
        file.write(lang)
        file.close()'''






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
        file = open("app_settings.json", "r")
        settings_str = file.read()
        file.close()
        settings_dict = json.loads(settings_str)
        language = settings_dict["language"]
        self.text_label_language = AppTranslator.translate_text("Select a language", language)

    def on_size(self, *args):
        self.overlay.size = self.size

    def res(self):
        self.App.get_running_app().restart()
