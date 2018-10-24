import os.path
import cv2
import csv
import http.client
import json

KS_CAPTCHA_TRAIN_FOLDER = "captchas_train"
KS_CAPTCHA_TRAIN_NUM = 250
KS_CAPTCHA_SOLVE_FOLDER = "captchas_solve"
KS_CAPTCHA_SOLVE_NUM = 250
KS_CAPTCHA_IMMUT_FOLDER = "captchas_immut"
KS_CAPTCHA_IMMUT_NUM = 250
KS_LETTERS_DST_FOLDER = "letters"
KS_MODEL_FILE = "model.hdf5"
KS_LABEL_FILE = "labels.dat"
KS_SOLVE_BASELINE = "solve_baseline.csv"
KS_IMMUT_BASELINE = "immut_baseline.csv"
KS_NUM_CAPTCHAS_ADD = 25

KS_APP_LOWEST_AVG_FOLDER = "app_lowest_avg"
KS_APP_RANDOM_FOLDER = "app_random"
KS_APP_LOWEST_LETTER_FOLDER = "app_lowest_letter"
KS_APP_LEAST_REP_FOLDER = "app_least_rep"
KS_APP_UNKNOWN_LOWEST_AVG_FOLDER = "app_unknown_lowest_avg"
KS_APP_UNKNOWN_RANDOM_FOLDER = "app_unknown_random"
KS_APP_UNKNOWN_LOWEST_LETTER_FOLDER = "app_unknown_lowest_letter"


IMAGE_SIZE = 20

def usedglyphs():
    return "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"

def openimage(path):
    filename = os.path.basename(path)
    filename_letters = os.path.splitext(filename)[0]
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, filename, filename_letters

def addborder(image, padX, padY):
    img = cv2.copyMakeBorder(image, padY, padY, padX, padX, cv2.BORDER_CONSTANT, value=[255,255,255])
    return img

def extractletters(image, filename, filename_letters):
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # https://docs.opencv.org/3.0.0/d4/d73/tutorial_py_contours_begin.html
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    letters = []
    for contour in contours:
        letters.append(cv2.boundingRect(contour))
    if len(letters) != len(filename_letters):
        print("detected {}, not {} letters in {}".format(len(letters), len(filename_letters), filename))
        return None, None
    letters = sorted(letters, key=lambda rect: rect[0])
    letter_imgs = []
    for rect, letter in zip(letters, filename_letters):
        x, y, w, h = rect
        letter_imgs.append(image[y - 2:y + h + 2, x - 2:x + w + 2])
    return letter_imgs, letters

def avginccounts(reader):
    rows = 0
    avg = 0.0
    inc = 0
    for row in reader:
        rows += 1
        avg += float(row["AVG"])
        if row["CORRECT"] == "False":
            inc += 1
    avg /= rows
    return avg, inc

def analyzefile(file):
    with open(file) as csv_file:
        reader = csv.DictReader(csv_file)
        _, incorrect = avginccounts(reader)
        return incorrect

def compareimmut(app_file):
    with open(KS_IMMUT_BASELINE) as immut_base:
        basereader = csv.DictReader(immut_base)
        baseavg, baseinc = avginccounts(basereader)

        with open(app_file) as app_res:
            appreader = csv.DictReader(app_res)
            appavg, appinc = avginccounts(appreader)

            print("Results went from avg of {:.4f} with {} incorrect to avg of {:.4f} with {} incorrect".format(baseavg, baseinc, appavg, appinc))

def sendtofirebase(url, data):
    conn = http.client.HTTPSConnection(url)

    payload = json.dumps(data)

    headers = {
        'Content-Type': "application/json",
        }

    conn.request("POST", "/smallbatch.json", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))