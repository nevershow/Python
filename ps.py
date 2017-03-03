# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
img = Image.open('tip.jpeg')
w, h = img.size
for x in range(0, w):
  for y in range(260, h):
    img.putpixel((x, y), (37,37,37))

drawBrush = ImageDraw.Draw(img)
# font = ImageFont.truetype(u"中山行书百年纪念版.ttf".encode('gbk'),49)
font = ImageFont.truetype(u"STXINGKA.TTF".encode('gbk'),49)
drawBrush.text((100,285), u"点击右上角", font=font)
drawBrush.text((50,350), u"在浏览器中打开", font=font)
img.save("tip1.jpeg")
