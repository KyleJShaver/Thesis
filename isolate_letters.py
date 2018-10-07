# STEP 2: Extract the letters from the captchas

import glob
import os.path
import cv2

src_folder = "bulk"
out_folder = "letters"
seen_letters = {}

files = glob.glob(os.path.join(src_folder, "*"))

for (i, file) in enumerate(files):
    filename = os.path.basename(file)
    filename_letters = os.path.splitext(filename)[0]
    img = cv2.imread(file)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.copyMakeBorder(grayscale, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
    thresh = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # https://docs.opencv.org/3.0.0/d4/d73/tutorial_py_contours_begin.html
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    letters = []
    for contour in contours:
        letters.append(cv2.boundingRect(contour))
    if len(letters) != len(filename_letters):
        print("detected {}, not {} letters in {}".format(len(letters), len(filename_letters), filename))
        continue
    letters = sorted(letters, key=lambda rect: rect[0])
    for rect, letter in zip(letters, filename_letters):
        x, y, w, h = rect
        letter_img = grayscale[y - 2:y + h + 2, x - 2:x + w + 2]
        out_path = os.path.join(out_folder, letter)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        seen = seen_letters.get(letter, 1)
        seen_letters[letter] = seen + 1
        png = os.path.join(out_path, str(seen).zfill(6) + ".png")
        cv2.imwrite(png, letter_img)