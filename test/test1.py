from kivy.config import Config
from kivy.properties import ColorProperty

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from PIL import Image
from kivy.graphics import Line, Ellipse, Rectangle, Color
from kivy.metrics import dp
from kivy.uix.widget import Widget

'''image_path = "color_image.jpg"  # Replace with the path to your image
image = Image.open(image_path)
pixel_color = image.getpixel((0, 380))
print(image.width, image.height)
print("RGB color:", pixel_color)'''
'''check_mark = "\\u2714"
print(check_mark)'''

'''base_settings = {"language": "fr",
                         "color_selector": "images/colorselector.png",
                         "color_part_background": "images/background_color_part.jpg",
                         "cursor_color_type": "images/cursor_green_slider.png"}

base_settings2 = {"language": "en",
                         "color_selector": "images/colorselector_2.png",
                         "color_part_background": "images/background_color_part.jpg",
                         "cursor_color_type": "images/cursor_green_slider.png"}

for i in base_settings.keys(), base_settings2.keys():
    print(i)'''

'''from removebg import RemoveBg

rmbg = RemoveBg("MDkF4RqRa4v5WoWrikdsfNu6", "error.log")
rmbg.remove_background_from_img_file("icone_support_logiciel.png")'''

"""from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.bubble import Bubble

Builder.load_string('''
<cut_copy_paste>
    size_hint: (None, None)
    size: (160, 120)
    pos_hint: {'center_x': .5, 'y': .6}
    BubbleContent:
        BubbleButton:
            text: 'Cut'
            size_hint_y: 1
        BubbleButton:
            text: 'Copy'
            size_hint_y: 1
        BubbleButton:
            text: 'Paste'
            size_hint_y: 1
''')


'''class cut_copy_paste(Bubble):
    pass


class BubbleShowcase(FloatLayout):

    def __init__(self, **kwargs):
        super(BubbleShowcase, self).__init__(**kwargs)
        self.but_bubble = Button(text='Press to show bubble')
        self.but_bubble.bind(on_release=self.show_bubble)
        self.add_widget(self.but_bubble)

    def show_bubble(self, *l):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = cut_copy_paste()
            self.add_widget(bubb)
        else:
            values = ('left_top', 'left_mid', 'left_bottom', 'top_left',
                'top_mid', 'top_right', 'right_top', 'right_mid',
                'right_bottom', 'bottom_left', 'bottom_mid', 'bottom_right')
            index = values.index(self.bubb.arrow_pos)
            self.bubb.arrow_pos = values[(index + 1) % len(values)]


class TestBubbleApp(App):

    def build(self):
        return BubbleShowcase()


if __name__ == '__main__':
    TestBubbleApp().run()"""

from kivy.app import App


class MainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.croper = WidgetCrop()
        self.add_widget(self.croper)

    def on_size(self, *args):
        self.croper.pos = self.center_x - self.croper.width/2, self.center_y - self.croper.height/2


class WidgetCrop(Widget):
    CORNER_CROP_WIDGET_SIZE = dp(15)
    LINE_WIDTH = dp(1.5)
    top_right_corner = None
    top_left_corner = None
    bottom_left_corner = None
    bottom_right_corner = None
    corner_color = ColorProperty()
    line_color = ColorProperty()

    def __init__(self, corner_color=(1, 1, 1, 1), line_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.size = 200, 200
        self.draw_canvas()
        self.corner_color = corner_color
        self.line_color = line_color

    def draw_canvas(self):
        with self.canvas:
            Color(rgba=self.line_color)
            Line(rectangle=(self.pos[0], self.pos[1], self.width, self.height), width=self.LINE_WIDTH)

            Color(rgba=self.corner_color)
            self.bottom_left_corner = Ellipse(pos=(self.pos[0]-self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]-self.CORNER_CROP_WIDGET_SIZE/2),
                    size=(self.CORNER_CROP_WIDGET_SIZE, self.CORNER_CROP_WIDGET_SIZE))

            self.top_left_corner = Ellipse(pos=(self.pos[0]-self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]+self.height-self.CORNER_CROP_WIDGET_SIZE/2),
                    size=(self.CORNER_CROP_WIDGET_SIZE, self.CORNER_CROP_WIDGET_SIZE))

            self.top_right_corner = Ellipse(pos=(self.pos[0] + self.width -self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]+self.height-self.CORNER_CROP_WIDGET_SIZE/2),
                    size=(self.CORNER_CROP_WIDGET_SIZE, self.CORNER_CROP_WIDGET_SIZE))

            self.bottom_right_corner = Ellipse(pos=(self.pos[0] +self.width - self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1] - self.CORNER_CROP_WIDGET_SIZE/2),
                    size=(self.CORNER_CROP_WIDGET_SIZE, self.CORNER_CROP_WIDGET_SIZE))

    def on_pos(self, *args):
        self.reset_draw()

    def on_touch_move(self, touch):
        self.verify_for_top_right_corner(touch.pos)
        self.verify_for_move_croper(touch.pos)
        self.verify_for_top_line(touch.pos)
        self.verify_for_right_line(touch.pos)
        self.verify_for_left_line(touch.pos)
        self.verify_for_bottom_line(touch.pos)
        self.verify_for_top_left_corner(touch.pos)
        self.verify_for_bottom_left_corner(touch.pos)
        self.verify_for_bottom_right_corner(touch.pos)

    def reset_draw(self):
        self.canvas.clear()
        self.draw_canvas()

    def verify_for_bottom_right_corner(self, touch_coordinates):
        placement_point_of_corner = self.bottom_right_corner.pos
        point_of_corner_at_top_height = (self.bottom_right_corner.pos[0] + self.CORNER_CROP_WIDGET_SIZE,
                                         self.bottom_right_corner.pos[1] + self.CORNER_CROP_WIDGET_SIZE)
        if placement_point_of_corner[0] <= touch_coordinates[0] <= point_of_corner_at_top_height[0] and placement_point_of_corner[1] <= touch_coordinates[1] <= point_of_corner_at_top_height[1]:
            self.width = touch_coordinates[0] - self.pos[0]
            previous_pos_y = self.pos[1]
            self.pos = self.pos[0], touch_coordinates[1]
            diff = self.pos[1] - previous_pos_y
            self.height = self.height - diff
            self.reset_draw()

    def verify_for_bottom_left_corner(self, touch_coordinates):
        placement_point_of_corner = self.bottom_left_corner.pos
        point_of_corner_at_top_height = (self.bottom_left_corner.pos[0] + self.CORNER_CROP_WIDGET_SIZE,
                                         self.bottom_left_corner.pos[1] + self.CORNER_CROP_WIDGET_SIZE)
        if placement_point_of_corner[0] <= touch_coordinates[0] <= point_of_corner_at_top_height[0] and placement_point_of_corner[1] <= touch_coordinates[1] <= point_of_corner_at_top_height[1]:
            previous_pos_x = self.pos[0]
            self.pos = touch_coordinates[0], self.pos[1]
            diff = self.pos[0] - previous_pos_x
            self.width = self.width - diff
            previous_pos_y = self.pos[1]
            self.pos = self.pos[0], touch_coordinates[1]
            diff = self.pos[1] - previous_pos_y
            self.height = self.height - diff
            self.reset_draw()

    def verify_for_top_left_corner(self, touch_coordinates):
        placement_point_of_corner = self.top_left_corner.pos
        point_of_corner_at_top_height = (self.top_left_corner.pos[0] + self.CORNER_CROP_WIDGET_SIZE,
                                         self.top_left_corner.pos[1] + self.CORNER_CROP_WIDGET_SIZE)
        if placement_point_of_corner[0] <= touch_coordinates[0] <= point_of_corner_at_top_height[0] and placement_point_of_corner[1] <= touch_coordinates[1] <= point_of_corner_at_top_height[1]:
            self.height = touch_coordinates[1] - self.pos[1]
            previous_pos_x = self.pos[0]
            self.pos = touch_coordinates[0], self.pos[1]
            diff = self.pos[0] - previous_pos_x
            self.width = self.width - diff
            self.reset_draw()

    def verify_for_top_right_corner(self, touch_coordinates):
        placement_point_of_corner = self.top_right_corner.pos
        point_of_corner_at_top_height = (self.top_right_corner.pos[0] + self.CORNER_CROP_WIDGET_SIZE,
                                         self.top_right_corner.pos[1] + self.CORNER_CROP_WIDGET_SIZE)

        if placement_point_of_corner[0] <= touch_coordinates[0] <= point_of_corner_at_top_height[0] and placement_point_of_corner[1] <= touch_coordinates[1] <= point_of_corner_at_top_height[1]:
            self.width = touch_coordinates[0]-self.pos[0]
            self.height = touch_coordinates[1]-self.pos[1]
            self.reset_draw()

    def verify_for_move_croper(self, touch_coordinates):
        point_left_bottom = self.pos[0]+self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]+self.CORNER_CROP_WIDGET_SIZE/2
        point_right_top = point_left_bottom[0]+self.width-self.CORNER_CROP_WIDGET_SIZE, point_left_bottom[1]+self.height-self.CORNER_CROP_WIDGET_SIZE

        if point_left_bottom[0] <= touch_coordinates[0] <= point_right_top[0] and point_left_bottom[1] <= touch_coordinates[1] <= point_right_top[1]:
            self.pos = touch_coordinates[0] - self.width / 2, touch_coordinates[1] - self.height / 2

    def verify_for_top_line(self, touch_coordinates):
        point_left_bottom = self.pos[0]+self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]+self.height-self.CORNER_CROP_WIDGET_SIZE/2
        point_right_top = point_left_bottom[0]+self.width-self.CORNER_CROP_WIDGET_SIZE/2, point_left_bottom[1]+self.CORNER_CROP_WIDGET_SIZE

        if point_left_bottom[0] <= touch_coordinates[0] <= point_right_top[0] and point_left_bottom[1] <= touch_coordinates[1] <= point_right_top[1]:
            self.height = touch_coordinates[1]-self.pos[1]
            self.reset_draw()

    def verify_for_right_line(self, touch_coordinates):
        point_left_bottom = self.pos[0]+self.width-self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]+self.CORNER_CROP_WIDGET_SIZE/2
        point_right_top = point_left_bottom[0]+self.CORNER_CROP_WIDGET_SIZE, point_left_bottom[1]+self.height-self.CORNER_CROP_WIDGET_SIZE/2

        if point_left_bottom[0] <= touch_coordinates[0] <= point_right_top[0] and point_left_bottom[1] <= touch_coordinates[1] <= point_right_top[1]:
            self.width = touch_coordinates[0]-self.pos[0]
            self.reset_draw()

    def verify_for_left_line(self, touch_coordinates):
        point_left_bottom = self.pos[0]-self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]+self.CORNER_CROP_WIDGET_SIZE/2
        point_right_top = point_left_bottom[0]+self.CORNER_CROP_WIDGET_SIZE, point_left_bottom[1]+self.height-self.CORNER_CROP_WIDGET_SIZE

        if point_left_bottom[0] <= touch_coordinates[0] <= point_right_top[0] and point_left_bottom[1] <= touch_coordinates[1] <= point_right_top[1]:
            previous_pos_x = self.pos[0]
            self.pos = touch_coordinates[0], self.pos[1]
            diff = self.pos[0]-previous_pos_x
            self.width = self.width-diff
            self.reset_draw()

    def verify_for_bottom_line(self, touch_coordinates):
        point_left_bottom = self.pos[0]+self.CORNER_CROP_WIDGET_SIZE/2, self.pos[1]-self.CORNER_CROP_WIDGET_SIZE/2
        point_right_top = point_left_bottom[0]+self.width-self.CORNER_CROP_WIDGET_SIZE, point_left_bottom[1]+self.CORNER_CROP_WIDGET_SIZE

        if point_left_bottom[0] <= touch_coordinates[0] <= point_right_top[0] and point_left_bottom[1] <= touch_coordinates[1] <= point_right_top[1]:
            previous_pos_y = self.pos[1]
            self.pos = self.pos[0], touch_coordinates[1]
            diff = self.pos[1] - previous_pos_y
            self.height = self.height - diff
            self.reset_draw()


class TestCropApp(App):
    def build(self):
        return MainWidget()


TestCropApp().run()
