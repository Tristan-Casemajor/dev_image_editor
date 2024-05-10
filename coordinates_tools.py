
def get_coef(real_width, width_in_gui):
    coef = real_width/width_in_gui
    print(coef)
    return coef


def calculation_of_real_coordinates(base_coordinates, image_pos, coef_image_size, image_height):
    x = (base_coordinates[0]-image_pos[0])*coef_image_size
    y = abs(base_coordinates[1]-image_pos[1]-image_height)*coef_image_size
    print(x, y)
    return x, y


def calculation_of_real_size_of_crop_widget(base_size, coef):
    real_width = base_size[0]*coef
    real_height = base_size[1]*coef
    print(real_width, real_height)
    return real_width, real_height
