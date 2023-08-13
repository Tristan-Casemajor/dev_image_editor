from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider

from app_translator import AppTranslator

Builder.load_file("color_creator.kv")

class ColorSlider(Slider):
    pass

class ColorImage(Image):
    pass

class ColorLayout(BoxLayout):
    text_hex_color = StringProperty("Hexadecimal")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language()

    def language(self):
        self.text_hex_color = AppTranslator.translate_text("Hexadecimal", "fr")
