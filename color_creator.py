import threading
from PIL import Image as Im  # Im to avoid conflicts with Kivy Image
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.uix.behaviors import CoverBehavior
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.clipboard import Clipboard
from app_translator import AppTranslator
from kivy.core.window import Window

Builder.load_file("color_creator.kv")


class ColorImage(Image):
    hex_color_input = ObjectProperty(None)
    alpha_slider = ObjectProperty(None)
    text_input_red1 = ObjectProperty(None)
    text_input_green1 = ObjectProperty(None)
    text_input_blue1 = ObjectProperty(None)
    text_input_red255 = ObjectProperty(None)
    text_input_green255 = ObjectProperty(None)
    text_input_blue255 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_size = []
        with self.canvas.after:
            # self.selector = Ellipse(size=(10, 10), pos=(10, 10))
            self.selector = Rectangle(pos=self.pos, size=(dp(19), dp(19)), source="images/colorselector.png")

    def image_color_selection(self, touch):
        if self.collide_point(*touch.pos):
            size = self.selector.size
            self.selector.pos = (touch.pos[0]-size[0]/2, touch.pos[1]-size[1]/2)
            '''if self.selector.pos[0] < self.selector.size[0]:
                print('yrbdb')
                self.selector.pos = self.selector.size[0], self.selector.pos[1]
            if self.selector.pos[0] > self.size[0]:
                self.selector.pos = self.width, self.selector.pos[1]'''
            try:
                image_select = Im.open("image_resized.jpg")
                color_rgb = image_select.getpixel((touch.pos[0]-self.pos[0], abs((touch.pos[1] - self.pos[1]) - self.height)))
                color_hex_rgb = "#{:02X}{:02X}{:02X}".format(*color_rgb)
                alpha = "{:02X}".format(int(self.alpha_slider.value))
                color_hex_rgba = color_hex_rgb + alpha
                self.hex_color_input.text = color_hex_rgba
                self.text_input_red1.text = str(round(color_rgb[0] / 255, 2))
                self.text_input_green1.text = str(round(color_rgb[1] / 255, 2))
                self.text_input_blue1.text = str(round(color_rgb[2] / 255, 2))
                self.text_input_red255.text = str(round(color_rgb[0], 2))
                self.text_input_green255.text = str(round(color_rgb[1], 2))
                self.text_input_blue255.text = str(round(color_rgb[2], 2))
            except Exception as e:
                print(e)
                print(touch.pos[0], touch.pos[1])
    def on_touch_down(self, touch):
        self.image_color_selection(touch)

    def on_touch_move(self, touch):
        self.image_color_selection(touch)


    def on_size(self, *args):
        size = self.selector.size
        self.selector.pos = self.center[0] - size[0] / 2, self.center[1] - size[1] / 2
        try:
            image = Im.open("images/color_image.jpg")
            size = (int(self.width), int(self.height))
            image_resize = image.resize(size)
            image_resize.save("image_resized.jpg")
        except:
            pass



class WidgetTest(Widget):
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
    hex_color = StringProperty("#00000000")
    list_value_brightness = []
    red1 = StringProperty("0")
    text_copy_button_hex = StringProperty("Copy")
    text_copy_button_rgba255 = StringProperty("Copy")
    text_copy_button_rgba1 = StringProperty("Copy")
    text_copy_button_when_text_copied = "Copied"
    text_copy_button_base = "copy"
    slider_scroll = ObjectProperty(None)
    scroll_view = ObjectProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()
        with self.canvas:
            Color(rgba=(0, 0, 0, 0.3))
            self.background = Rectangle(pos=self.pos)

    def set_slider_opacity(self):
        if Window.height >= 815:
            self.slider_scroll.opacity = 0
        else:
            self.slider_scroll.opacity = 1

    def on_size(self, *args):
        self.set_slider_opacity()
        self.background.size = self.size


    def language(self):
        lang = "es"
        self.text_hex_color = AppTranslator.translate_text("Hexadecimal", lang)
        self.slider_red_title = AppTranslator.translate_text("Red", lang)
        self.slider_green_title = AppTranslator.translate_text("Green", lang)
        self.slider_blue_title = AppTranslator.translate_text("Blue", lang)
        self.slider_alpha_title = AppTranslator.translate_text("Transparency", lang)
        self.slider_brightness_title = AppTranslator.translate_text("Brightness", lang)
        self.text_copy_button_when_text_copied = AppTranslator.translate_text("Copied", lang)
        self.text_copy_button_base = AppTranslator.translate_text("Copy", lang)
        self.text_copy_button_hex = self.text_copy_button_base
        self.text_copy_button_rgba255 = self.text_copy_button_base
        self.text_copy_button_rgba1 = self.text_copy_button_base

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


    def get_hex_color(self, red, green, blue, alpha, name="", actual_color=""):
        if name != "alpha":
            rgba = (int(red), int(green), int(blue), int(alpha))
            hex = '#{:02x}{:02x}{:02x}{:02x}'.format(*rgba)
            self.hex_color = hex
        else:
            alpha_value = '{:02x}'.format(int(alpha))
            self.hex_color = actual_color[0:7] + alpha_value

    def copy_color_to_clipboard(self, value, color_format, name=""):  # name allow to make the difference between the RGBA255 copy button and RBGA1 copy button
        if color_format == "hex":
            Clipboard.copy(value)
            self.text_copy_button_hex = self.text_copy_button_when_text_copied
        elif color_format == "rgba":
            Clipboard.copy(f"{value[0]}, {value[1]}, {value[2]}, {value[3]}")

        if name == "rgba1":
                self.text_copy_button_rgba1 = self.text_copy_button_when_text_copied
        elif name == "rgba255":
            self.text_copy_button_rgba255 = self.text_copy_button_when_text_copied
        Clock.schedule_once(self.reset_copy_button_text, 1.6)

    def reset_copy_button_text(self, dt):
        tuple_copy_button_text = [self.text_copy_button_hex,
                                  self.text_copy_button_rgba255,
                                  self.text_copy_button_rgba1]
        if self.text_copy_button_hex == self.text_copy_button_when_text_copied:
            self.text_copy_button_hex = self.text_copy_button_base
        if self.text_copy_button_rgba255 == self.text_copy_button_when_text_copied:
            self.text_copy_button_rgba255 = self.text_copy_button_base
        if self.text_copy_button_rgba1 == self.text_copy_button_when_text_copied:
            self.text_copy_button_rgba1 = self.text_copy_button_base

    def on_alpha_slider(self, *args):
        self.alpha_slider.value = 255
