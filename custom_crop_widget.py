from kivy.properties import ColorProperty
from kivy.graphics import Line, Ellipse, Rectangle, Color
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class WidgetCrop(Widget):
    CORNER_CROP_WIDGET_SIZE = dp(15)
    LINE_WIDTH = dp(1.5)
    top_right_corner = None
    top_left_corner = None
    bottom_left_corner = None
    bottom_right_corner = None
    corner_color = ColorProperty()
    line_color = ColorProperty()

    def __init__(self, corner_color=(0.4, 0.4, 0.4, 1), line_color=(0.4, 0.4, 0.4, 1), **kwargs):
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
        self.verify_for_croper_size()

    def reset_draw(self):
        self.canvas.clear()
        self.draw_canvas()

    def verify_for_croper_size(self):
        if self.height < dp(30):
            self.height = dp(30)

        if self.width < dp(30):
            self.width = dp(30)

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