import json


def get_settings():
    file = open("app_settings.json", "r", encoding="utf-8")
    dict_settings_str = file.read()
    file.close()
    dict_settings = json.loads(dict_settings_str)
    return dict_settings
