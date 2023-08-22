from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from plyer import filechooser
from image_work_dir_manager import ImageWorkDirManager
from os import listdir, getcwd, chdir, path
from PIL import Image as Im   # to avoid conflicts between Kivy Image and PIL image

Builder.load_file("image_editing.kv")


class LayoutSelectImagePath(BoxLayout):
    path_to_image = StringProperty("")
    def select_image(self):
        # the file chooser return a list on selected files
        app_work_dir = getcwd()
        path_image = filechooser.open_file(title="choose an image",
                                     filters=[("Image", "*.jpg", "*.png", "*.ico", "*.bmp")])
        chdir(app_work_dir)
        if len(path_image) > 0:
            self.path_to_image = path_image[0]
            ImageWorkDirManager().copy_image_to_work_dir(self.path_to_image, "image_work_dir")


class ButtonWithImageAtCenter(Button):
    image_source = StringProperty("")

class WidgetImage(Widget):
    image_work = ObjectProperty(None)

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


class LayoutControlWidget(BoxLayout):
    pass


class LayoutImageEditing(BoxLayout):
    pass

