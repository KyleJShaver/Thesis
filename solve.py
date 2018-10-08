from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy
import imutils
import cv2
import pickle
import os.path

model_savefile = "model.hdf5"
model_labelfile = "labels.dat"
captcha_src = "captchas_solve"

with open(model_labelfile, "rb") as labels:
    lb = pickle.load(labels)

model = load_model(model_savefile)
captchas = list(paths.list_images(captcha_src))
for captcha in captchas:
    filename = os.path.basename(captcha)
    filename_letters = os.path.splitext(filename)[0]
    image = cv2.imread(captcha)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # https://docs.opencv.org/3.0.0/d4/d73/tutorial_py_contours_begin.html
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    letters = []
    for contour in contours:
        letters.append(cv2.boundingRect(contour))
    if len(letters) != len(filename_letters):
        print("detected {}, not {} letters in {}".format(len(letters), len(filename_letters), filename))
        continue
    letters = sorted(letters, key=lambda rect: rect[0])


    output = cv2.merge([image] * 3)
    predictions = []
    for rect, letter in zip(letters, filename_letters):
        x, y, w, h = rect
        letter_img = image[y - 2:y + h + 2, x - 2:x + w + 2]
        letter_img = resize_to_fit(letter_img, 20, 20)

        letter_img = numpy.expand_dims(letter_img, axis=2)
        letter_img = numpy.expand_dims(letter_img, axis=0)
        prediction = model.predict(letter_img)
        letter = lb.inverse_transform(prediction)[0]
        max = numpy.amax(prediction)
        if max < .8:
            print("woah!")
        predictions.append(letter)
        cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
        cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    captcha_text = "".join(predictions)
    if captcha_text != filename_letters:
        print("Captcha is {} but should be {}".format(captcha_text, filename_letters))

'''
    # Show the annotated image
    cv2.imshow("Output", output)
    cv2.waitKey(30000)
'''