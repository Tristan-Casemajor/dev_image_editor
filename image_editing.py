import os
import threading
from kivy.uix.label import Label
from app_translator import AppTranslator
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, Clock, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from plyer import filechooser
from image_work_dir_manager import ImageWorkDirManager
from os import listdir, getcwd, chdir, path
from kivy.utils import get_color_from_hex
from PIL import Image as Im   # Im to avoid conflicts between Kivy Image and PIL image
from custom_crop_widget import WidgetCrop
from image_engine import ActionBuilder
from coordinates_tools import *

Builder.load_file("image_editing.kv")


# This Layout allow the user to select an image file, the file is copy to the image_work_dir folder
class LayoutSelectImagePath(BoxLayout):
    path_to_image = StringProperty("")

    def select_image(self):
        # We use getcwd() and chdir() because plyer's filechooser change the work directory of the app
        # so the good work directory is saved before the use of filechooser and it replace the wrong
        # work directory after the use of the filechooser.
        app_work_dir = getcwd()
        path_image = filechooser.open_file(filters=[("Image", "*.jpg", "*.png", "*.ico", "*.bmp", "*.gif")])
        chdir(app_work_dir)
        if len(path_image) > 0:
            self.path_to_image = path_image[0]
            ImageWorkDirManager().copy_image_to_work_dir(self.path_to_image, "image_work_dir")


class LabelImage(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = self.texture_size
        self.font_name = "fonts/arial_unicode_ms.ttf"

    def on_touch_move(self, touch):
        point_left_bottom = self.pos[0]-self.texture_size[0]/2, self.pos[1]-self.texture_size[1]/2
        point_top_right = self.pos[0]+self.texture_size[0]/2, self.pos[1]+self.texture_size[1]/2
        if point_left_bottom[0] <= touch.pos[0] <= point_top_right[0] and point_left_bottom[1] <= touch.pos[1] <= point_top_right[1]:
            self.pos = touch.pos




# custom button with an image at the center, to use it ou must pass the path
# to the image you want in the image_source property
class ButtonWithImageAtCenter(Button):
    image_source = StringProperty("")


class ScrollViewWithScrollBarLayout(BoxLayout):
    widget_image_layout = ObjectProperty(None)



# This widget contais the image selected by the user
class WidgetImage(Widget):
    image_work = ObjectProperty(None)
    crop_widget = WidgetCrop()
    label_widget = LabelImage()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_image, 1/2)
        Clock.schedule_interval(self.verify_crop_widget_pos, 1/60)
        Clock.schedule_interval(self.verify_label_image_pos, 1/60)

    def verify_crop_widget_pos(self, dt):
        image_position = self.image_work.pos
        image_size = self.image_work.size
        if self.crop_widget.pos[0] < image_position[0]:
            self.crop_widget.pos[0] = image_position[0]
        if self.crop_widget.pos[1] < image_position[1]:
            self.crop_widget.pos[1] = image_position[1]
        if self.crop_widget.height < image_size[1] and self.crop_widget.pos[1]+self.crop_widget.height > image_position[1] + image_size[1]:
            self.crop_widget.pos[1] = image_position[1] + image_size[1] - self.crop_widget.height
        if self.crop_widget.width < image_size[0] and self.crop_widget.pos[0]+self.crop_widget.width > image_position[0] + image_size[0]:
            self.crop_widget.pos[0] = image_position[0] + image_size[0] - self.crop_widget.width

    def verify_label_image_pos(self, dt):
        image_position = self.image_work.pos
        image_size = self.image_work.size
        if self.label_widget.pos[0]-self.label_widget.texture_size[0]/2 < image_position[0]:
            self.label_widget.pos[0] = image_position[0]+self.label_widget.texture_size[0]/2

        if self.label_widget.pos[1]+self.label_widget.texture_size[1]/2 < image_position[1]:
            self.label_widget.pos[1] = image_position[1]+self.label_widget.texture_size[1]/2

        point_top_right = self.label_widget.pos[0] + self.label_widget.texture_size[0]/2, self.label_widget.pos[1] + self.label_widget.texture_size[1]/2

        if point_top_right[1] > image_position[1]+image_size[1]:
            self.label_widget.pos[1] = (image_position[1]+image_size[1])-self.label_widget.texture_size[1]/2

        if point_top_right[0] > image_position[0]+image_size[0]:
            self.label_widget.pos[0] = (image_position[0] + image_size[0])-self.label_widget.texture_size[0]/2

    def update_image(self, dt):
        list_images_work_dir = listdir("image_work_dir")
        if len(list_images_work_dir) > 0:
            self.image_work.source = path.join("image_work_dir", list_images_work_dir[0])
            self.image_work.reload()
            self.set_image_size(list_images_work_dir[0])

    def set_image_size(self, image_name):
        widget_size = self.size
        image = Im.open(path.join(ImageWorkDirManager.work_image_path, image_name))
        image_base_size = image.size
        # to display the image with the good size we calculate a coefficient (coef)
        # coef = measurement_exceeded / widget_measurement_exceeded
        # with the coef we divide the hight and the width of the image to keep the ratio and
        # to have an image whi don't exceed the size of his container
        if image_base_size[0] <= widget_size[0] and image_base_size[1] <= widget_size[1]:
            self.image_work.size = image_base_size

        if image_base_size[1] > widget_size[1]:
            coef = image_base_size[1]/widget_size[1]
            self.image_work.size = image_base_size[0]/coef, image_base_size[1]/coef

        if image_base_size[0] > widget_size[0]:
            coef = image_base_size[0] / widget_size[0]
            self.image_work.size = image_base_size[0] / coef, image_base_size[1] / coef

        if image_base_size[0] > widget_size[0] and image_base_size[1] > widget_size[1]:
            coef1 = image_base_size[0] / widget_size[0]
            coef2 = image_base_size[1] / widget_size[1]
            if coef1 > coef2:
                self.image_work.size = image_base_size[0] / coef1, image_base_size[1] / coef1
            else:
                self.image_work.size = image_base_size[0] / coef2, image_base_size[1] / coef2

    def add_remove_crop_widget(self, state):
        self.crop_widget.pos = self.center_x-self.crop_widget.width/2, self.center_y-self.crop_widget.height/2
        if state == "down":
            self.add_widget(self.crop_widget)
        else:
            self.remove_widget(self.crop_widget)

    def add_remove_text_label(self, state):
        self.label_widget.pos = self.center_x - self.label_widget.width / 2, self.center_y - self.label_widget.height / 2
        if state == "down":
            self.add_widget(self.label_widget)
        else:
            self.remove_widget(self.label_widget)

    def update_text(self, text):
        self.label_widget.text = text

    def checkbox_activity_control(self, current_widget, *args):
        if current_widget.state == "normal":
            pass
        else:
            for widget in args:
                if widget == current_widget:
                    pass
                else:
                    widget.state = "normal"

    def reset_size_values(self, width, height):
        width.text = ""
        height.text = ""

    def proceed(self, rm_bg_state, rm_bg_api_key, resize_state, new_width, new_height,
                reframe_state, add_text_state, text, rotate_state, angle, 
                modify_output_state, output_format, add_overlay_state, color, 
                name_new_image, saving_path, exe_state, path_to_exe):

        crop_widget_base_coordinates = self.crop_widget.pos
        label_add_text_base_coordinates = self.label_widget.pos

        rm_bg_state_bool = False if rm_bg_state == "normal" else True
        resize_state_bool = False if resize_state == "normal" else True
        reframe_state_bool = False if reframe_state == "normal" else True
        add_text_state_bool = False if add_text_state == "normal" else True
        rotate_state_bool = False if rotate_state == "normal" else True
        modify_output_state_bool = False if modify_output_state == "normal" else True
        add_overlay_state_bool = False if add_overlay_state == "normal" else True
        exe_state_bool = False if exe_state == "normal" else True

        print("PROCEED")
        coef = get_coef(Im.open(ImageWorkDirManager().give_path_to_image()).width, self.image_work.width)
        real_coordinates_crop_widget = calculation_of_real_coordinates(crop_widget_base_coordinates, self.image_work.pos, coef, self.image_work.height)
        real_size_crop_widget = calculation_of_real_size_of_crop_widget(self.crop_widget.size, coef)

        real_cordinates_label_text = calculation_of_real_coordinates(label_add_text_base_coordinates, self.image_work.pos, coef, self.image_work.height)

        '''ActionBuilder().build_action_list(rm_bg_state_bool, rm_bg_api_key, resize_state_bool, new_width, new_height,
                reframe_state_bool, add_text_state_bool, text, rotate_state_bool, angle,
                modify_output_state_bool, output_format, add_overlay_state_bool, color,
                name_new_image, saving_path, exe_state_bool, path_to_exe)'''




    '''def proceed(self):
        print(self.label_widget.pos)
        print(self.label_widget.text)'''



# This Layout contains all the widget with wich the user can select options to modufy the image he selected
class LayoutControlWidget(BoxLayout):
    text_select_image = StringProperty("Image to edit")
    text_remove_bg = StringProperty("Remove background")
    text_api_key_remove_bg = StringProperty("Api key")
    text_resize = StringProperty("Resize")
    text_resize_keep_ratio = StringProperty("Keep ratio")
    text_resize_do_not_keep_ratio = StringProperty("Do not keep ratio")
    text_resize_width = StringProperty("Width")
    text_resize_height = StringProperty("Height")
    text_crop = StringProperty("Reframe")
    add_text = StringProperty("Add a text area")
    rotate_image = StringProperty("Rotate image")
    text_rotate_angle = StringProperty("Angle")
    text_output_format = StringProperty("Modify output format (png by default)")
    text_overlay = StringProperty("Add color overlay")
    text_color_overlay = StringProperty("Color")
    new_name_of_image = StringProperty("Name of the new image")
    save_image_as = StringProperty("Save the image as")
    text_exe_file_icon = StringProperty("Add the image as an icon to an .exe file")
    text_path_to_exe_file = StringProperty("Path to the exe file")
    text_proceed_button = StringProperty("Proceed")
    color_preview = ColorProperty((0, 0, 0, 0.5))
    path_to_folder = StringProperty("")
    path_to_exe_file = StringProperty("")
    widget_image_layout = ObjectProperty(None)
    text_input_width = ObjectProperty(None)
    text_input_height = ObjectProperty(None)
    keep_ratio_checkbox = ObjectProperty(None)
    api_key_text_input = ObjectProperty(None)
    file_last_value_change = os.path.join(".temp", "last_value_change.txt")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()
        Clock.schedule_interval(self.keep_ratio_calculator, 1/2)
        Clock.schedule_once(self.set_api_key, 2)

    def language(self):
        language = AppTranslator.get_current_language()
        self.text_select_image = AppTranslator().translate_text(self.text_select_image, language)
        self.text_remove_bg = AppTranslator().translate_text(self.text_remove_bg, language)
        self.text_api_key_remove_bg = AppTranslator().translate_text(self.text_api_key_remove_bg, language)
        self.text_resize_keep_ratio = AppTranslator().translate_text(self.text_resize_keep_ratio, language)
        self.text_resize_do_not_keep_ratio = AppTranslator().translate_text(self.text_resize_do_not_keep_ratio, language)
        self.text_resize_width = AppTranslator().translate_text(self.text_resize_width, language)
        self.text_resize_height = AppTranslator().translate_text(self.text_resize_height, language)
        self.add_text = AppTranslator().translate_text(self.add_text, language)
        self.text_crop = AppTranslator().translate_text(self.text_crop, language)
        self.rotate_image = AppTranslator().translate_text(self.rotate_image, language)
        self.text_rotate_angle = AppTranslator().translate_text(self.text_rotate_angle, language)
        self.text_output_format = AppTranslator().translate_text(self.text_output_format, language)
        self.text_overlay = AppTranslator().translate_text(self.text_overlay, language)
        self.text_color_overlay = AppTranslator().translate_text(self.text_color_overlay, language)
        self.new_name_of_image = AppTranslator().translate_text(self.new_name_of_image, language)
        self.save_image_as = AppTranslator().translate_text(self.save_image_as, language)
        self.text_exe_file_icon = AppTranslator().translate_text(self.text_exe_file_icon, language)
        self.text_path_to_exe_file = AppTranslator().translate_text(self.text_path_to_exe_file, language)

        if language == "fr":
            self.text_resize = "Redimensionner"
            self.text_proceed_button = "Lancer"
        elif language == "uk":
            self.text_resize = AppTranslator().translate_text(self.text_resize, language)
            self.text_proceed_button = AppTranslator().translate_text(self.text_proceed_button, language)
        else:
            self.text_resize = AppTranslator().translate_text(self.text_resize, language)
            self.text_proceed_button = AppTranslator().translate_text(self.text_proceed_button, language)


    def set_color_preview(self, color):
        try:
            self.color_preview = get_color_from_hex(color)
        except:
            pass

    def select_folder_new_picture(self):
        app_work_dir = getcwd()
        path_folder = filechooser.choose_dir()
        chdir(app_work_dir)
        print(path_folder)
        if len(path_folder) > 0:
            self.path_to_folder = path_folder[0]

    def select_path_to_exe_file(self):
        app_work_dir = getcwd()
        path_exe = filechooser.open_file(filters=[("exe file", "*.exe", "*.dll")])
        chdir(app_work_dir)
        if len(path_exe) > 0:
            self.path_to_exe_file = path_exe[0]

    def keep_ratio_calculator(self, dt):

        if self.keep_ratio_checkbox.state == "down":
            try:
                file = open(self.file_last_value_change, "r")
                data = file.read()
                file.close()
                image = Im.open(ImageWorkDirManager().give_path_to_image())
                image_base_size = image.size
            except:
                pass

            else:
                if data == "height":
                    try:
                        new_height = float(self.text_input_height.text)
                    except:
                        pass
                    else:
                        base_height = image_base_size[1]
                        coef = new_height/base_height
                        base_width = image_base_size[0]
                        self.text_input_width.text = str(int(coef*base_width))
                        file = open(self.file_last_value_change, "w")
                        file.write("height")
                        file.close()
                else:
                    try:
                        new_width = float(self.text_input_width.text)
                    except:
                        pass
                    else:
                        base_width = image_base_size[0]
                        coef = new_width / base_width
                        base_height = image_base_size[1]
                        self.text_input_height.text = str(int(coef * base_height))
                        file = open(self.file_last_value_change, "w")
                        file.write("width")
                        file.close()

    def last_value(self, widget):
        if widget.name == "width":
            file = open(self.file_last_value_change, "w")
            file.write("width")
            file.close()
        else:
            file = open(self.file_last_value_change, "w")
            file.write("height")
            file.close()

    def save_api_key(self, api_key):
        file = open(os.path.join("user_data", "api_key.txt"), "w")
        file.write(api_key)
        file.close()

    def set_api_key(self, dt):
        file = open(os.path.join("user_data", "api_key.txt"), "r")
        key = file.read()
        file.close()
        self.api_key_text_input.text = key


class LayoutImageEditing(BoxLayout):
    pass
