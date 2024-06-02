from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from time import strftime
from kivy.lang import Builder


class Test(TabbedPanel):
    pass


class ClockTest(BoxLayout):
    time_str = ObjectProperty()
    tm_interval = 3610  # 5 seconds
    tm_flag = True
    tm = tm_interval

    def __init__(self, **kwargs):
        super(ClockTest, self).__init__(**kwargs)
        Clock.schedule_interval(self.cb, 0)

    def cb(self, dt):
        if self.tm_flag:
            self.tm -= dt
            if self.tm <= 0:
                self.tm = self.tm_interval
                print('tm: ', self.tm)
                m, s = divmod(self.tm, 60)
                self.time_str.text = ('%02d:%02d.%02d' %
                                      (int(m), int(s), int(s * 100 % 100)))
                print('time_str: ', self.time_str.text)

                # loop: for time delay
                for x in range(100000):
                    text = strftime('[b]%H[/b]:%M:%S')

        m, s = divmod(self.tm, 60)
        self.time_str.text = ('%02d:%02d.%02d' %
                              (int(m), int(s), int(s * 100 % 100)))


class ClockTest1App(App):
    def build(self):
        tm_obj = Test()

        return tm_obj


if __name__ == '__main__':
    ClockTest1App().run()