import threading
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_image, 1/2)

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        thread_lang = threading.Thread(target=self.language)
        thread_lang.start()

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


class LayoutImageEditing(BoxLayout):
    pass
