import time
import traceback
from image_work_dir_manager import ImageWorkDirManager
from PIL import Image, ImageDraw
import os
from removebg import RemoveBg
import shutil

class Engine:
    work_dir = "image_engine_work_dir"
    work_dir_remove_background = os.path.join("image_engine_work_dir", "remove_bg_work_dir")

    def rotation(self, angle, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            image_modified = image.rotate(angle, resample=Image.BICUBIC, expand=True)
            path = self.get_saving_path(extension)
            image_modified.save(path, quality=100)
            image.close()
            self.remove_previous_image(image_path)
        except:
            traceback.print_exc()
            return 1

    def resize(self, width, height, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            image_modified = image.resize((int(width), int(height)), resample=Image.LANCZOS)
            path = self.get_saving_path(extension)
            image_modified.save(path, quality=100)
            image.close()
            self.remove_previous_image(image_path)
        except Exception as e:
            traceback.print_exc()
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
            image.close()
            self.remove_previous_image(image_path)
        except:
            return 3

    def remove_background(self, api_key, extension):
        image_path = self.get_image_path()
        image = Image.open(image_path)
        image_work_path = os.path.join(self.work_dir_remove_background, "work.png")
        image.save(image_work_path)
        try:
            remove_bg_tool = RemoveBg(api_key, "error.log")
            remove_bg_tool.remove_background_from_img_file(image_work_path)

            for file in os.listdir(self.work_dir):
                if os.path.isfile(os.path.join(self.work_dir, file)):
                    image.close()
                    os.remove(os.path.join(self.work_dir, file))

        except Exception as e:
            for i in os.listdir(self.work_dir_remove_background):
                image.close()
                os.remove(os.path.join(self.work_dir_remove_background, i))
            return 4

        else:
            image2 = Image.open(os.path.join(self.work_dir_remove_background, "work.png_no_bg.png"))
            saving_path = self.get_saving_path(extension)
            image2.save(saving_path)

            for i in os.listdir(self.work_dir_remove_background):
                image.close()
                os.remove(os.path.join(self.work_dir_remove_background, i))

    def reframe(self):
        pass

    def add_text_area(self):
        pass

    def get_saving_path(self, extension):
        return os.path.join(self.work_dir, "work"+"."+extension)

    def get_image_path(self):
        files_in_image_engine_work_dir = os.listdir(self.work_dir)
        if len(files_in_image_engine_work_dir) >= 2:
            for i in files_in_image_engine_work_dir:
                if os.path.isfile(os.path.join(self.work_dir, i)):
                    return os.path.join(self.work_dir, i)
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

    def remove_previous_image(self, path):
        if ImageWorkDirManager.work_image_path in path:
            return
        else:
            if len(os.listdir(self.work_dir)) >= 3:
                os.remove(path)


class ActionBuilder:
    pass
