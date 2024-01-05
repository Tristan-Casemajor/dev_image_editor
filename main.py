from kivy import Config
Config.set('graphics', 'width', '880')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'minimum_width', '790')
Config.set('graphics', 'minimum_height', '300')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.utils import get_color_from_hex
from settings_app_manager import SettingsManager
import os
from image_work_dir_manager import ImageWorkDirManager
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, NumericProperty, ColorProperty
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget
from app_translator import AppTranslator
import threading
from image_engine import Engine


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
        current_language = AppTranslator().get_current_language()
        if current_language != "en":
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
        Clock.schedule_once(self.remove_splashscreen, 8)

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
        self.tab_images = AppTranslator().translate_text(self.tab_images, language)
        self.tab_color = AppTranslator().translate_text(self.tab_color, language)
        self.tab_settings = AppTranslator().translate_text(self.tab_settings, language)


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


class TabbedPanelItemMainGui(TabbedPanelItem):
    tabs_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_color_tabs()

    def set_color_tabs(self):
        color = SettingsManager().get_settings().get("tabs_color")
        if len(color[1::]) == 6:
            try:
                self.tabs_color = get_color_from_hex(color)
            except:
                self.tabs_color = (0.1, 0.8, 0.15, 1)
        elif len(color[1::]) == 8:
            try:
                self.tabs_color = get_color_from_hex(color)
            except:
                self.tabs_color = (0.1, 0.8, 0.15, 1)


class DevImageEditApp(App):
    def on_start(self):
        self.check_folder(".temp")
        self.check_folder(ImageWorkDirManager.work_image_path)
        self.check_folder(Engine.work_dir)
        self.check_folder(os.path.join(Engine.work_dir, "remove_bg_work_dir"))
        self.check_folder_without_deletion("user_data")
        SettingsManager().check_settings_file()

    def on_stop(self):
        self.check_folder(".temp")
        self.check_folder(ImageWorkDirManager.work_image_path)
        self.check_folder(Engine.work_dir)
        self.check_folder(os.path.join(Engine.work_dir, "remove_bg_work_dir"))
        self.check_folder_without_deletion("user_data")

    def build(self):
        self.icon = "images/logo_dev_icon_editor.jpg"
        self.title = "Dev Image Editor"
        return Gui()

    # This function verify existence of somes app folder (important folder) and delete his
    # content at the start and at the shutdown of the app
    # do not modify this function
    @staticmethod
    def check_folder(folder_path):
        folder_exist = os.path.exists(folder_path)
        if folder_exist:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path) and file_path != os.path.join(Engine.work_dir, "remove_bg_work_dir"):
                    os.rmdir(file_path)
        else:
            os.mkdir(folder_path)

    @staticmethod
    def check_folder_without_deletion(folder_path):
        folder_exist = os.path.exists(folder_path)
        if folder_exist:
            return
        else:
            os.mkdir(folder_path)


DevImageEditApp().run()
