# STEP 2: Extract the letters from the captchas

import glob
import os.path
import cv2
import common

src_folder = "captchas"
out_folder = "letters"



def isolateletters(infolder, outfolder, manualcaptchas):
    seen_letters = {}
    files = glob.glob(os.path.join(infolder, "*"))

    if manualcaptchas is not None:
        files = manualcaptchas

    for (_, file) in enumerate(files):
        image, filename, filename_letters = common.openimage(file)
        image = common.addborder(image, 10, 10)
        letter_imgs, letters = common.extractletters(image, filename, filename_letters)
        for (i, letter_img) in enumerate(letter_imgs):
            out_path = os.path.join(outfolder, filename_letters[i])
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            seen = seen_letters.get(filename_letters[i], 1)
            seen_letters[filename_letters[i]] = seen + 1
            png = os.path.join(out_path, str(seen).zfill(6) + ".png")
            cv2.imwrite(png, letter_img)


#isolateletters(src_folder, out_folder)