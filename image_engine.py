import traceback

from image_work_dir_manager import ImageWorkDirManager
from PIL import Image, ImageDraw
import os
from removebg import RemoveBg

class Engine:
    work_dir = "image_engine_work_dir"

    def rotation(self, angle, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            image_modified = image.rotate(angle)
            path = self.get_saving_path(extension)
            image_modified.save(path, quality=100)
        except:
            return 1

    def resize(self, width, height, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            image_modified = image.resize((int(width), int(height)))
            path = self.get_saving_path(extension)
            image_modified.save(path, quality=100)
        except:
            return 2

    def add_color_overlay(self, color, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            overlay_color = self.hex_to_rgba(color)
            overlay = Image.new('RGBA', image.size, overlay_color)
            image_modified = Image.alpha_composite(image.convert('RGBA'), overlay)
            path = self.get_saving_path(extension)
            image_modified.save(path, quality=100)
        except:
            return 3

    def remove_background(self, api_key, extension):
        try:
            image_path = self.get_image_path()
            print(image_path)
            remove_bg_tool = RemoveBg(api_key, "error.log")
            remove_bg_tool.remove_background_from_img_file(image_path)
            image = Image.open(os.path.join("image_work_dir", "work.jpg_no_bg.png"))
            if extension not in ["png", "gif", "bmp"]:
                path = self.get_saving_path("png")
                image.save(path)
            else:
                path = self.get_saving_path(extension)
                image.save(path)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 4
        os.remove(os.path.join("image_work_dir", "work.jpg_no_bg.png"))

    def get_saving_path(self, extension):
        return os.path.join(self.work_dir, "work"+"."+extension)

    def get_image_path(self):
        files_in_image_engine_work_dir = os.listdir(self.work_dir)
        if files_in_image_engine_work_dir:
            return os.path.join(self.work_dir, files_in_image_engine_work_dir[0])
        else:
            return ImageWorkDirManager().give_path_to_image()

    @staticmethod
    def hex_to_rgba(hex_code):
        hex_code = hex_code.lstrip('#')

        red = int(hex_code[0:2], 16)
        green = int(hex_code[2:4], 16)
        blue = int(hex_code[4:6], 16)
        alpha = int(hex_code[6:8], 16) if len(hex_code) == 8 else 255

        return red, green, blue, alpha


class ActionBuilder:
    pass
