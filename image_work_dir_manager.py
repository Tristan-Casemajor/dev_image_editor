import shutil
import os

class ImageWorkDirManager:
    work_image_path = "image_work_dir"

    def copy_image_to_work_dir(self, image_path, work_dir_path):
        for filename in os.listdir(work_dir_path):
            file_path = os.path.join(work_dir_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        work_file_name = "work." + self.get_extension_of_image(os.path.basename(image_path))
        shutil.copyfile(image_path, work_dir_path+"\\"+work_file_name)

    @staticmethod
    def get_extension_of_image(image_name):
        list_image_name = image_name.split(".")
        return list_image_name[-1]

    def give_path_to_image(self):
        for filename in os.listdir(self.work_image_path):
            if "work" in filename:
                return os.path.join(self.work_image_path, filename)
            else:
                return None


