from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random

size = (172, 56)
darkestgray = 255
lightestgray = 255
color = False
wobble = 0
num = 1

def randval(small, big):
    return random.randint(small, big)

def randdec(small, big):
    return randval(small * 100, big * 100) / 100.0
def gen(num):
    for _ in range(0, num):
        img = Image.new("RGBA", size, "white")
        draw = ImageDraw.Draw(img)
        for x in range(0, size[0] - 1):
            for y in range(0, size[1] - 1):
                r = randval(darkestgray,lightestgray)
                g, b  = r, r
                if color is True:
                    g = randval(darkestgray,lightestgray)
                    b = randval(darkestgray,lightestgray)
                img.putpixel((x,y), (r, g, b, 255))
        font = ImageFont.truetype("Roboto-Regular.ttf", 32)
        glyphs = "QWERTYUIOPASDFGHJKLZXCVBNM123456789"
        s = ""
        for _ in range(0,6):
            s += glyphs[random.randint(0,len(glyphs) - 1)]
        textimg = Image.new("RGBA", size, (0,0,0,0))
        textdraw = ImageDraw.Draw(textimg)
        textdraw.text((randval(10,30), randval(4,10)),s,(0,0,0),font=font)
        rotated = textimg.rotate(randdec(-wobble,wobble), expand=0)
        img = Image.alpha_composite(img, rotated)
        if num > 1:
            img.save("bulk/"+s+".png")
        else:
            img.save('out.png')

gen(num)