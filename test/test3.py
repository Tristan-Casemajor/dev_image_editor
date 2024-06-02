from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class CursorChangeApp(App):
    def build(self):
        label = Label(text="Survolez-moi pour changer le curseur")

        # Fonction pour changer le curseur lorsque la souris survole le Label
        def change_cursor(entered):
            if entered:
                Window._system_cursor = 'size_nw_se'
            else:
                Window._system_cursor = 'arrow'

        label.bind(on_enter=lambda instance: change_cursor(True))
        label.bind(on_leave=lambda instance: change_cursor(False))

        return label

if __name__ == '__main__':
    CursorChangeApp().run()