import threading
import json
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, Clock, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.behaviors import CoverBehavior  # not use in this file but use in the kv file, do not remove this line
from kivy.uix.widget import Widget
from app_translator import AppTranslator
from settings_app_manager import SettingsManager

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

class WidgetSelectorWithCheckBox(Widget):
    image_source = StringProperty("")
    check_box_selector = ObjectProperty(None)
    selector_name = StringProperty("")
    list_check_box = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_selector, 4)

    def on_check_box_selector(self, *args):
        self.list_check_box.append(self.check_box_selector)

    def init_selector(self, dt):
        current_selector = SettingsManager().get_settings().get("color_selector")
        print(current_selector)
        for i in self.list_check_box:
            if i.name == current_selector:
                i.active = True

    def set_selector(self, widget):
        current_selector = SettingsManager().get_settings().get("color_selector")
        if widget.active:
            current_selector = widget.name
            SettingsManager().update_settings({"color_selector": current_selector})
            checks_box = self.list_check_box
            self.list_check_box = []
            for i in checks_box:
                if i.name != current_selector:
                    i.active = False
                self.list_check_box.append(i)
        elif widget.name == current_selector and not widget.active:
            widget.active = True

class LayoutApplyChange(BoxLayout):
    height_depend_change = NumericProperty(0)
    red = NumericProperty(0)
    green = NumericProperty(0)
    blue = NumericProperty(0)
    alpha = NumericProperty(0)
    text_reboot = StringProperty("")
    icon_size = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings_app = SettingsManager().get_settings()
        Clock.schedule_interval(self.verify_change, 1.2)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.text_reboot = ""
            self.red = 0
            self.green = 0
            self.blue = 0
            self.alpha = 0
            self.height_depend_change = 0
            self.icon_size = 0

    def verify_change(self, dt):
        actual_dict_settings = SettingsManager().get_settings()
        if actual_dict_settings == self.settings_app:
            pass
        else:
            self.height_depend_change = dp(25)
            self.red = 0.09
            self.green = 0.92
            self.blue = 0.44
            self.alpha = 1
            self.icon_size = dp(20)
            self.text_reboot = AppTranslator().translate_text("close and reopen the application to apply changes",
                                                              actual_dict_settings["language"])
            self.settings_app = actual_dict_settings


class SettingsLayout(BoxLayout):
    text_label_language = StringProperty("Select a language")
    text_label_cursor = StringProperty("Select a color selector")

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
        self.text_label_cursor = AppTranslator().translate_text("Select a color selector", language)

    def on_size(self, *args):
        self.overlay.size = self.size

    def res(self):
        self.App.get_running_app().restart()
