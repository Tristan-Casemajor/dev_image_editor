from kivy import Config
Config.set('graphics', 'width', '880')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'minimum_width', '790')
Config.set('graphics', 'minimum_height', '300')
import json
from get_settings_app import get_settings
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Rectangle, Color, Line
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, NumericProperty
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from app_translator import AppTranslator
import threading

class LayoutWarningLanguage(BoxLayout):
    height_depend_language_aviable = NumericProperty(0)
    red = NumericProperty(0)
    green = NumericProperty(0)
    blue = NumericProperty(0)
    alpha = NumericProperty(0)
    text_warning = StringProperty("")
    icon_size = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if AppTranslator.test_language:
            pass
        else:
            self.height_depend_language_aviable = dp(25)
            self.red = 0.92
            self.green = 0.66
            self.blue = 0
            self.alpha = 1
            self.text_warning = AppTranslator().get_warning()
            self.icon_size = dp(20)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.text_warning = ""
            self.red = 0
            self.green = 0
            self.blue = 0
            self.alpha = 0
            self.height_depend_language_aviable = 0
            self.icon_size = 0



class Gui(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.splashscreen = SplashScreen()
        self.add_widget(self.splashscreen)
        self.main_gui = MainTabbedPanel()
        self.main_gui.opacity = 0
        self.add_widget(self.main_gui)
        self.warning = LayoutWarningLanguage()
        self.warning.opacity = 0
        self.add_widget(self.warning)
        Clock.schedule_once(self.remove_splashscreen, 6)

    def on_size(self, *args):
        self.splashscreen.size = self.size
        self.main_gui.size = self.size

    def remove_splashscreen(self, dt):
        self.splashscreen.opacity = 0
        self.main_gui.opacity = 1
        self.warning.opacity = 1


class MainTabbedPanel(TabbedPanel):
    tab_images = StringProperty("Image Editing")
    tab_color = StringProperty("Color Creation")
    tab_settings = StringProperty("Application Settings")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()

    def language(self):
        language = AppTranslator.get_current_language()
        self.tab_images = AppTranslator().translate_text("Image Editing", language)
        self.tab_color = AppTranslator().translate_text("Color Creation", language)
        self.tab_settings = AppTranslator().translate_text("Application Settings", language)


class SplashScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.rectangle_background = Rectangle(pos=self.pos, size=self.size, source="images/background_splashscreen.png")
        self.image_splashscreen = Image(source="images/logo_dev_icon_editor_without_background.png", size=(dp(170), dp(170)))
        self.loading_anim = Image(source="images/loading_anim.gif", size=(dp(220), dp(220)), anim_delay=1/33)
        self.add_widget(self.image_splashscreen)
        self.add_widget(self.loading_anim)

    def on_size(self, *args):
        self.rectangle_background.size = self.size
        self.image_splashscreen.pos = (self.center_x-self.image_splashscreen.width/2, self.center_y-self.image_splashscreen.height/2)
        self.loading_anim.pos = self.center_x-self.loading_anim.width/2, self.center_y/20


class DevImageEditApp(App):
    def on_start(self):
        self.check_temp_folder()

    def on_stop(self):
        self.check_temp_folder()

    def build(self):
        self.icon = "images/logo_dev_icon_editor.jpg"
        self.title = "Dev Image Editor"
        return Gui()

    # This function verift existence of .temp folder (important folder) and delete his
    # content et the start and at the shutdown of the app
    # do not modify this function
    @staticmethod
    def check_temp_folder():
        temp_folder_exist = os.path.exists(".temp")
        if temp_folder_exist:
            folder_path = ".temp"
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
        else:
            os.mkdir(".temp")
    '''@staticmethod
    def check_settings_file():
        setting_file_exist = os.path.exists("app_settings.json")
        base_settings = {"language": "fr",
                         "color_selector": "images/colorselector.png",
                         "color_part_background": "images/background_color_part.jpg",
                         "cursor_color_type": "images/cursor_green_slider.png"}
        if setting_file_exist:
            dict_settings = get_settings()
            for dict_settings in'''


DevImageEditApp().run()
