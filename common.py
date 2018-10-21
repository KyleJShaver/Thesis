import os.path
import cv2
import csv

KS_CAPTCHA_TRAIN_FOLDER = "captchas_train"
KS_CAPTCHA_TRAIN_NUM = 10000
KS_CAPTCHA_SOLVE_FOLDER = "captchas_solve"
KS_CAPTCHA_SOLVE_NUM = 10000
KS_CAPTCHA_IMMUT_FOLDER = "captchas_immut"
KS_CAPTCHA_IMMUT_NUM = 10000
KS_LETTERS_DST_FOLDER = "letters"
KS_MODEL_FILE = "model.hdf5"
KS_LABEL_FILE = "labels.dat"
KS_SOLVE_BASELINE = "solve_baseline.csv"
KS_IMMUT_BASELINE = "immut_baseline.csv"
KS_NUM_CAPTCHAS_ADD = 1000

KS_APP_LOWEST_AVG_FOLDER = "app_lowest_avg"
KS_APP_LOWEST_AVG_LETTERS = os.path.join(KS_APP_LOWEST_AVG_FOLDER, "letters")
KS_APP_LOWEST_AVG_MODEL = os.path.join(KS_APP_LOWEST_AVG_FOLDER, KS_MODEL_FILE)
KS_APP_LOWEST_AVG_LABEL = os.path.join(KS_APP_LOWEST_AVG_FOLDER, KS_LABEL_FILE)
KS_APP_LOWEST_AVG_IMMUT = os.path.join(KS_APP_LOWEST_AVG_FOLDER, "immut.csv")

KS_APP_RANDOM_FOLDER = "app_random"
KS_APP_RANDOM_LETTERS = os.path.join(KS_APP_RANDOM_FOLDER, "letters")
KS_APP_RANDOM_MODEL = os.path.join(KS_APP_RANDOM_FOLDER, KS_MODEL_FILE)
KS_APP_RANDOM_LABEL = os.path.join(KS_APP_RANDOM_FOLDER, KS_LABEL_FILE)
KS_APP_RANDOM_IMMUT = os.path.join(KS_APP_RANDOM_FOLDER, "immut.csv")

KS_APP_LOWEST_LETTER_FOLDER = "app_lowest_letter"
KS_APP_LOWEST_LETTER_LETTERS = os.path.join(KS_APP_LOWEST_LETTER_FOLDER, "letters")
KS_APP_LOWEST_LETTER_MODEL = os.path.join(KS_APP_LOWEST_LETTER_FOLDER, KS_MODEL_FILE)
KS_APP_LOWEST_LETTER_LABEL = os.path.join(KS_APP_LOWEST_LETTER_FOLDER, KS_LABEL_FILE)
KS_APP_LOWEST_LETTER_IMMUT = os.path.join(KS_APP_LOWEST_LETTER_FOLDER, "immut.csv")

KS_APP_LEAST_REP_FOLDER = "app_least_rep"
KS_APP_LEAST_REP_LETTERS = os.path.join(KS_APP_LEAST_REP_FOLDER, "letters")
KS_APP_LEAST_REP_MODEL = os.path.join(KS_APP_LEAST_REP_FOLDER, KS_MODEL_FILE)
KS_APP_LEAST_REP_LABEL = os.path.join(KS_APP_LEAST_REP_FOLDER, KS_LABEL_FILE)
KS_APP_LEAST_REP_IMMUT = os.path.join(KS_APP_LEAST_REP_FOLDER, "immut.csv")

IMAGE_SIZE = 20

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

def compareimmut(app_file):
    with open(KS_IMMUT_BASELINE) as immut_base:
        basereader = csv.DictReader(immut_base)
        baseavg, baseinc = avginccounts(basereader)

    with open(app_file) as app_res:
        appreader = csv.DictReader(app_res)
        appavg, appinc = avginccounts(appreader)

    print("Results went from avg of {:.4f} with {} incorrect to avg of {:.4f} with {} incorrect".format(baseavg, baseinc, appavg, appinc))