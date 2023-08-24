import json
import os


# The SettingsManager class manage all settings of the app except the language who is managed by the AppTranslator class
class SettingsManager:
    base_settings = {"language": "en",
                     "color_selector": "images/colorselector.png",
                     "color_part_background": "images/background_color_part.jpg",
                     "cursor_color_type": "images/cursor_green_slider.png",
                     "tabs_color": "0.1, 0.8, 0.15, 1"}

    def check_settings_file(self):
        try:
            self.__get_an_error()
        except:
            self.reset_settings()
        else:
            setting_file_exist = os.path.exists("app_settings.json")
            if setting_file_exist:
                list_dict_settings_key = list(self.get_settings())
                list_test = []
                if len(list_dict_settings_key) == len(list(self.base_settings)):
                    for i in list_dict_settings_key:
                        if i in list(self.base_settings):
                            list_test.append(True)
                        else:
                            list_test.append(False)
                    if all(list_test):
                        return
                    else:
                        self.reset_settings()
                else:
                    self.reset_settings()
            else:
                self.reset_settings()

    def reset_settings(self):
        settings_str = json.dumps(self.base_settings)
        file = open("app_settings.json", "w", encoding="utf-8")
        file.write(settings_str)
        file.close()

    def get_settings(self):
        try:
            file = open("app_settings.json", "r", encoding="utf-8")
            dict_settings_str = file.read()
            file.close()
            dict_settings = json.loads(dict_settings_str)
        except:
            dict_settings = self.base_settings

        return dict_settings

    @staticmethod
    def __get_an_error():
        file = open("app_settings.json", "r", encoding="utf-8")
        dict_settings_str = file.read()
        file.close()
        dict_settings = json.loads(dict_settings_str)

    def update_settings(self, new_setting):
        try:
            setting_name = list(new_setting)
            if not isinstance(new_setting, dict):
                print(1/0)
        except:
            return
        else:
            if setting_name[0] in list(self.base_settings):
                current_settings = self.get_settings()
                current_settings.update(new_setting)
                new_settings_str = json.dumps(current_settings)
                file = open("app_settings.json", "w", encoding="utf-8")
                file.write(new_settings_str)
                file.close()


