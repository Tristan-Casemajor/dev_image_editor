import json
from translate import Translator


class AppTranslator:

    @staticmethod
    def test_language_aviable():
        try:
            translator = Translator(to_lang="fr")
            text_translate = translator.translate("red")
            test_translation_aviable = text_translate
            if "YOU USED ALL AVAILABLE FREE TRANSLATIONS" not in test_translation_aviable:
                return True
            else:
                return False
        except:
            return False

    test_language = test_language_aviable()

    def translate_text(self, text, language):
        current_language = AppTranslator.get_current_language()
        if self.test_language and current_language != "en":
            file = open("test1.txt", "w")
            file.close()
            try:
                translator = Translator(to_lang=language)
                text_translate = translator.translate(text)
            except:
                return text
            else:
                file = open("test2.txt", "w")
                file.close()
                return text_translate
        else:
            file = open("test_final.txt", "w")
            file.close()
            return text

    @staticmethod
    def get_current_language():
        file = open("app_settings.json", "r")
        settings_str = file.read()
        file.close()
        settings_dict = json.loads(settings_str)
        language = settings_dict["language"]
        return language

    @staticmethod
    def set_current_language(language):
        file = open("app_settings.json", "r")
        settings_str = file.read()
        file.close()
        settings_dict = json.loads(settings_str)
        settings_dict["language"] = language
        new_settings_str = json.dumps(settings_dict)
        file = open("app_settings.json", "w")
        file.write(new_settings_str)
        file.close()

    def get_warning(self):
        if self.test_language:
            return "ok"
        else:
            try:
                translator = Translator(to_lang="fr")
                text_translate = translator.translate("red")
            except:
                current_language = self.get_current_language()
                file = open("warning_message.json", "r", encoding="utf-8")
                dict_message_str = file.read()
                file.close()
                dict_message = json.loads(dict_message_str)
                dict_message_1 = dict_message["message_no_internet"]
                try:
                    return dict_message_1[current_language]
                except:
                    return "Impossible to translate the UI (no internet connection)"
            else:
                current_language = self.get_current_language()
                file = open("warning_message.json", "r", encoding="utf-8")
                dict_message_str = file.read()
                file.close()
                dict_message = json.loads(dict_message_str)
                dict_message_2 = dict_message["message_to_many_call"]
                try:
                    return dict_message_2[current_language]
                except:
                    return "Quota exceeded for UI translations, try again later."


if __name__ == "__main__":
    print("This API use translate Python module to translate the UI of Dev Image Editor")
    print("You can use this API to translate any UI of your choice")