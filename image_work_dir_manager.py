import shutil
import os

class ImageWorkDirManager:
    work_image_path = "image_work_dir"

    def copy_image_to_work_dir(self, image_path, work_dir_path):
        work_file_name = "work." + self.get_extension_of_image(os.path.basename(image_path))
        shutil.copyfile(image_path, work_dir_path+"\\"+work_file_name)

    @staticmethod
    def get_extension_of_image(image_name):
        list_image_name = image_name.split(".")
        return list_image_name[-1]