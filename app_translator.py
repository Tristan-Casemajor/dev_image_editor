from translate import Translator


class AppTranslator:
    @staticmethod
    def translate_text(text, language):
        try:
            translator = Translator(to_lang=language)
            text_translate = translator.translate(text)
        except:
            return text
        else:
            return text_translate



print(AppTranslator.translate_text("Rouge", "fr"))