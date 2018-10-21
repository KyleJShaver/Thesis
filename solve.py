#STEP 4: Use the model to predict captcha

from keras.models import load_model
from imutils import paths
import numpy
import cv2
import pickle
import os.path
import csv
import common


model_savefile = "model.hdf5"
model_labelfile = "labels.dat"
captcha_src = "captchas_solve"
conf_out = "confidence.csv"

def solve(inmodelfile, inlabelfile, incaptchas, outconfcsv):
    if os.path.exists(outconfcsv):
        os.remove(outconfcsv)
    with open(outconfcsv, mode="w") as conf_csv:
        writer = csv.writer(conf_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["CAPTCHA","PREDICTED","CORRECT","CONF1","CONF2","CONF3","CONF4","AVG"])

    with open(inlabelfile, "rb") as labels:
        lb = pickle.load(labels)

    model = load_model(inmodelfile)
    captchas = list(paths.list_images(incaptchas))
    for captcha in captchas:
        image, filename, filename_letters = common.openimage(captcha)
        image = common.addborder(image, 10, 10)

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
        confidence = []
        avg = 0
        for rect, letter in zip(letters, filename_letters):
            x, y, w, h = rect
            letter_img = image[y - 2:y + h + 2, x - 2:x + w + 2]
            letter_img = cv2.resize(letter_img, (common.IMAGE_SIZE, common.IMAGE_SIZE))

            letter_img = numpy.expand_dims(letter_img, axis=2)
            letter_img = numpy.expand_dims(letter_img, axis=0)
            prediction = model.predict(letter_img)
            letter = lb.inverse_transform(prediction)[0]
            conf = numpy.amax(prediction)
            confidence.append(conf)
            avg += conf
            predictions.append(letter)
            cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
            cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        captcha_text = "".join(predictions)
        avg /= len(confidence)
        confidence.append(avg)
        with open(outconfcsv, mode="a") as conf_csv:
            writer = csv.writer(conf_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([filename_letters, captcha_text, filename_letters == captcha_text] + confidence)

#solve(model_savefile, model_labelfile, captcha_src, conf_out)