from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

img = Image.open("test.jpg")
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("segoe_ui_bold.ttf", 16)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((111, 200),"Sample Text",(0,0,0),font=font)
img.save('sample-out.jpg')