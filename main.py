from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanel
from app_translator import AppTranslator
import threading


class MainTabbedPanel(TabbedPanel):
    tab_images = StringProperty("Image Editing")
    tab_color = StringProperty("Color Creation")
    tab_param = StringProperty("Application Settings")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()
    def language(self):
        pass
        '''
        self.tab_images = AppTranslator.translate_text("Image Editing", "fr")
        self.tab_color = AppTranslator.translate_text("Color Creation", "fr")
        self.tab_param = AppTranslator.translate_text("Application Settings", "fr")'''


class DevImageEditApp(App):
    def on_start(self):
        print("start")

    def on_stop(self):
        print("stop")

    def build(self):
        self.icon = "images/logo_dev_icon_editor.jpg"
        self.title = "Dev Image Editor"


DevImageEditApp().run()