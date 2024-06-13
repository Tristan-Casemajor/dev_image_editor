import os
os.environ['KIVY_NO_ARGS'] = '1'
from kivy.config import Config
Config.set('graphics', 'window_state', 'invisible')
from kivy.metrics import dp
import time
import traceback
from image_work_dir_manager import ImageWorkDirManager
from PIL import Image, ImageDraw, ImageFont
import os
from removebg import RemoveBg
import shutil



class Engine:
    work_dir = "image_engine_work_dir"
    work_dir_remove_background = os.path.join("image_engine_work_dir", "remove_bg_work_dir")
    ressource_hacker_abs_path = os.path.abspath("ResourceHacker.exe")

    def rotation(self, angle, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            image_modified = image.rotate(angle, resample=Image.BICUBIC, expand=True)
            path = self.get_saving_path(extension)
            # image_modified.save(path, quality=100)
            self.save_image(image_modified, path)
            image.close()
            self.remove_previous_image(image_path)
        except:
            return 1

    def resize(self, width, height, extension):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            image_modified = image.resize((int(width), int(height)), resample=Image.LANCZOS)
            path = self.get_saving_path(extension)
            self.save_image(image_modified, path)
            image.close()
            self.remove_previous_image(image_path)
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
            self.save_image(image_modified, path)
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

    def reframe(self, crop_widget_real_coordinates, crop_widget_real_size, extension):
        try:
            # TODO : replace dp(15) by the dp(15) from custon_crop_widget.py
            image_path = self.get_image_path()
            image = Image.open(image_path)
            left = round(crop_widget_real_coordinates[0])
            #top = round(abs(image.height-crop_widget_real_coordinates[1])-dp(15)/2)
            top = round(crop_widget_real_coordinates[1] - crop_widget_real_size[1]-dp(15)/2)
            bottom = round(crop_widget_real_coordinates[1]) #round(top + crop_widget_real_size[1]-dp(15)/2)
            right = round(left + crop_widget_real_size[0])
            image_modified = image.crop((left, top, right, bottom))
            path = self.get_saving_path(extension)
            self.save_image(image_modified, path)
            image.close()
            self.remove_previous_image(image_path)
        except:
            return 5

    def add_text_area(self, text, extension, label_text_real_coordinates, label_text_real_size):
        try:
            image_path = self.get_image_path()
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("fonts/segoe_ui_bold.ttf", 30)
            x = label_text_real_coordinates[0]-label_text_real_size[0]
            y = label_text_real_coordinates[1]+label_text_real_size[1]
            draw.text((x, y), text, (0, 0, 0), font=font)
            path = self.get_saving_path(extension)
            self.save_image(image, path)
            image.close()
            self.remove_previous_image(image_path)
        except:
            return 6


    def add_image_to_exe_file(self, path_to_exe, a):
        try:
            icone = self.get_saving_path("ico")
            icone_abs_path = os.path.abspath(icone)
            exe_dir = self.get_exe_dir(path_to_exe)
            app_dir = os.getcwd()
            os.chdir(exe_dir)
            os.system(f"{self.ressource_hacker_abs_path} -open {path_to_exe} -save exe_file_temp_1.exe -action delete -res {path_to_exe} -mask Icon,Icon Group")
            os.system(f"{self.ressource_hacker_abs_path} -open exe_file_temp_1.exe -save exe_file_temp_2.exe -action addoverwrite -res {icone_abs_path} -mask ICONGROUP,MAINICON")
            os.system(f"{self.ressource_hacker_abs_path} -open {path_to_exe} -save extracted_manifest.bin -action extract -mask MANIFEST,1")
            os.system(f"{self.ressource_hacker_abs_path} -open exe_file_temp_2.exe -save exe_file_with_ico.exe -action addoverwrite -res extracted_manifest.bin -mask MANIFEST,1")
            time.sleep(3)
            os.remove("exe_file_temp_1.exe")
            os.remove("exe_file_temp_2.exe")
            os.remove("extracted_manifest.bin")
            os.chdir(app_dir)
        except:
            pass

    def get_saving_path(self, extension):
        return os.path.join(self.work_dir, "work"+"."+extension)

    def get_exe_dir(self, path):
        path_split = path.split("\\")
        dir_path_list = path_split[0:-1]
        dir_path_str = "\\".join(dir_path_list)
        return dir_path_str


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

    def save_image(self, image, path):
        try:
            image.save(path, quality=100)
        except:
            image_modified_rgb = image.convert('RGB') # to convert PNG (RGBA) to JPG (RGB)
            image_modified_rgb.save(path, quality=100)

    def save_image_to_user_path_selected(self, name, path, extension):
        name = self.vefify_file_name(name, extension)
        source = self.get_image_path()
        destination = f"{path}\\{name}"
        shutil.copy2(source, destination)

    @staticmethod
    def vefify_file_name(name, extension):
        if not name.isspace or name not in ["con", "prn", "CON", "PRN", "AUX", "aux", "NUL", "nul", "COM1", "COM2",
                                            "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9"]:
            for i in name:
                if i in ["/", "\\", ":", "*", "?", '"', ">", "<", "|"]:
                    name = f"refactor.{extension}"
                    return name
            name = f"{name}.{extension}"
            return name
        else:
            name = f"refactor.{extension}"
            return name

class ActionBuilder:
    ENGINE = Engine()

    def build_action_list(self, rm_bg_state_bool, rm_bg_api_key, resize_state_bool, new_width, new_height,
                reframe_state_bool, crop_widget_real_coordinates, crop_widget_real_size, add_text_state_bool, text,
                label_text_real_coordinates, label_text_real_size, rotate_state_bool, angle,
                modify_output_state, output_format, add_overlay_state_bool, color,
                name_new_image, saving_path, exe_state_bool, path_to_exe):
        actions = []
        args = []
        if add_text_state_bool:
            actions.append(self.ENGINE.add_text_area)
            args.append((text, output_format, label_text_real_coordinates, label_text_real_size))
        if reframe_state_bool:
            actions.append(self.ENGINE.reframe)
            args.append((crop_widget_real_coordinates, crop_widget_real_size, output_format))
        if resize_state_bool:
            actions.append(self.ENGINE.resize)
            args.append((new_width, new_height, output_format))
        if rm_bg_state_bool:
            actions.append(self.ENGINE.remove_background)
            args.append((rm_bg_api_key, output_format))
        if add_overlay_state_bool:
            actions.append(self.ENGINE.add_color_overlay)
            args.append((color, output_format))
        if rotate_state_bool:
            actions.append(self.ENGINE.rotation)
            args.append((angle, output_format))
        if exe_state_bool:
            actions.append(self.ENGINE.add_image_to_exe_file)
            args.append((path_to_exe, ""))

        self.run_action_list(actions, args, name_new_image, saving_path, output_format, exe_state_bool)

    def run_action_list(self, actions, args, name, path, extension, exe_state_bool):
        index = 0
        for action in actions:
            action(*args[index])
            index += 1

        if not exe_state_bool:
            self.ENGINE.save_image_to_user_path_selected(name, path, extension)
