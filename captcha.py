# STEP 1: Generate the captchas

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random
import os.path

size = (172, 56)
darkestgray = 255
lightestgray = 255
color = False
wobble = 10

num_letters = 4
percent_notifier = .05
'''
out_folder = "captchas"
num = 10000
'''
out_folder = "captchas_solve"
num = 1000


def randval(small, big):
    return random.randint(small, big)

def randdec(small, big):
    return randval(small * 100, big * 100) / 100.0

def usedglyphs():
    return "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
def gen(num):
    next_percent = percent_notifier
    for i in range(0, num):
        if (i * 1.0) / (num * 1.0) >= next_percent:
            next_percent += percent_notifier
            print("completed: " + str(i))
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
        glyphs = usedglyphs()
        x_pos = 0
        filename = ""
        img
        for ltr in range(0,num_letters):
            textimg = Image.new("RGBA", size, (0, 0, 0, 0))
            s = glyphs[random.randint(0,len(glyphs) - 1)]
            filename += s
            textdraw = ImageDraw.Draw(textimg)
            x_pos += randval(10,15) + 20
            fonts = ["Roboto-Regular.ttf", "Lora-Bold.ttf", "Arvo-Regular.ttf"]
            font = ImageFont.truetype(fonts[randval(0, len(fonts)-1)], 20)
            textdraw.text((x_pos, randval(10, 20)), s, (0, 0, 0), font=font)
            rotated = textimg.rotate(randdec(-wobble, wobble), expand=0)
            img = Image.alpha_composite(img, rotated)
        if num > 1:
            out_path = os.path.join(out_folder, filename)
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
            img.save(out_path + ".png")
        else:
            img.save('out.png')

gen(num)