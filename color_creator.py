import threading

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider

from app_translator import AppTranslator

Builder.load_file("color_creator.kv")

class ColorImage(Image):
    pass

class ColorLayout(BoxLayout):
    text_hex_color = StringProperty("Hexadecimal")
    text_rgb_color = StringProperty("RGBA")  # for RGB (0-255) and RGB (0-1)
    slider_red_title = StringProperty("Red")
    slider_green_title = StringProperty("Green")
    slider_blue_title = StringProperty("Blue")
    slider_alpha_title = StringProperty("transparency")
    slider_brightness_title = StringProperty("brightness")
    red_slider = ObjectProperty(None)
    green_slider = ObjectProperty(None)
    blue_slider = ObjectProperty(None)
    alpha_slider = ObjectProperty(None)
    brightness_slider = ObjectProperty(None)
    hex_color = StringProperty("")
    list_value_brightness = []


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()

    def language(self):
        lang = "en"
        self.text_hex_color = AppTranslator.translate_text("Hexadecimal", lang)
        self.slider_red_title = AppTranslator.translate_text("Red", lang)
        self.slider_green_title = AppTranslator.translate_text("Green", lang)
        self.slider_blue_title = AppTranslator.translate_text("Blue", lang)
        self.slider_alpha_title = AppTranslator.translate_text("Transparency", lang)
        self.slider_brightness_title = AppTranslator.translate_text("Brightness", lang)
        if lang == "ru":
            self.text_rgb_color = "РГБА"
        elif lang == "fr":
            self.text_rgb_color = "RVBA"
        else:
            self.text_rgb_color = AppTranslator.translate_text("RGBA", lang)


    def test_value(self, value):
        try:
            test = float(value)
            if not 0 <= test <= 255:
                return False
        except:
            return False
        else:
            return True

    def set_brightness(self, value_brightness):
        self.list_value_brightness.append(value_brightness)
        last_value = self.list_value_brightness[-1]
        if len(self.list_value_brightness) >= 3:
            penultimate_value = self.list_value_brightness[-2]
        else:
            penultimate_value = 0
        if last_value-penultimate_value > 0:
            if not 0 < self.red_slider.value <= 1:
                self.red_slider.value -= 0.5 * (last_value - penultimate_value)
            if not 0 < self.green_slider.value <= 1:
                self.green_slider.value -= 0.5 * (last_value - penultimate_value)
            if not 0 < self.blue_slider.value <= 1:
                self.blue_slider.value -= 0.5 * (last_value - penultimate_value)
        else:
            if self.red_slider.value != 0:
                self.red_slider.value += 0.5 * (penultimate_value - last_value)
            if self.green_slider.value != 0:
                self.green_slider.value += 0.5 * (penultimate_value - last_value)
            if self.blue_slider.value != 0:
                self.blue_slider.value += 0.5 * (penultimate_value - last_value)

        if self.red_slider.value < 0:
            self.red_slider.value = 0
        elif self.red_slider.value > 255:
            self.red_slider.value = 255
        if self.green_slider.value < 0:
            self.green_slider.value = 0
        elif self.green_slider.value > 255:
            self.green_slider.value = 255
        if self.blue_slider.value < 0:
            self.blue_slider.value = 0
        elif self.blue_slider.value > 255:
            self.blue_slider.value = 255


    def get_hex_color(self, red, green, blue, alpha):
        rgba = (int(red), int(green), int(blue), int(alpha))
        hex = '#{:02x}{:02x}{:02x}{:02x}'.format(*rgba)
        self.hex_color = hex
