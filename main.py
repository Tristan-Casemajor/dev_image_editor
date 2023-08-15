from kivy import Config
Config.set('graphics', 'width', '880')
Config.set('graphics', 'height', '560')
Config.set('graphics', 'minimum_width', '790')
Config.set('graphics', 'minimum_height', '300')
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, ObjectProperty
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget

from app_translator import AppTranslator
import threading

class Gui(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.splashscreen = SplashScreen()
        self.add_widget(self.splashscreen)
        self.main_gui = MainTabbedPanel()
        self.main_gui.opacity = 0
        self.add_widget(self.main_gui)
        Clock.schedule_once(self.remove_splashscreen, 6)
    def on_size(self, *args):
        self.splashscreen.size = self.size
        self.main_gui.size = self.size

    def remove_splashscreen(self, dt):
        self.splashscreen.opacity = 0
        self.main_gui.opacity = 1


class MainTabbedPanel(TabbedPanel):
    tab_images = StringProperty("Image Editing")
    tab_color = StringProperty("Color Creation")
    tab_param = StringProperty("Application Settings")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()

    def language(self):
        #pass
        lang = "en"
        self.tab_images = AppTranslator.translate_text("Image Editing", lang)
        self.tab_color = AppTranslator.translate_text("Color Creation", lang)
        self.tab_param = AppTranslator.translate_text("Application Settings", lang)


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
        print("start")

    def on_stop(self):
        print("stop")

    def build(self):
        self.icon = "images/logo_dev_icon_editor.jpg"
        self.title = "Dev Image Editor"




DevImageEditApp().run()