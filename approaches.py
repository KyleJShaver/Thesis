import common

import csv
import os
from random import shuffle

def getprops(folder):
    props = dict()
    props["folder"] = folder
    props["letters"] = os.path.join(folder, "letters")
    props["model"] = os.path.join(folder, common.KS_MODEL_FILE)
    props["labels"] = os.path.join(folder, common.KS_LABEL_FILE)
    props["immut"] = os.path.join(folder, "immut.csv")
    return props

def random():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        shuffle(rows)
        rand = rows[:common.KS_NUM_CAPTCHAS_ADD]
        rand = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", rand))
        return rand

def lowest_average():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        rows = sorted(rows, key=lambda a: a["AVG"])
        lowest = rows[:common.KS_NUM_CAPTCHAS_ADD]
        lowest = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", lowest))
        return lowest

def lowest_letter():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            row["MIN"] = min(float(row["CONF1"]), float(row["CONF2"]), float(row["CONF3"]), float(row["CONF4"]))
            rows.append(row)
        rows = sorted(rows, key=lambda a: a["MIN"])
        lowest = rows[:common.KS_NUM_CAPTCHAS_ADD]
        lowest = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", lowest))
        return lowest

def least_rep():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        shuffle(rows)
        dirlist = os.listdir(common.KS_LETTERS_DST_FOLDER)
        minnum = common.KS_CAPTCHA_SOLVE_NUM * 4
        minfolder = ""
        for folder in dirlist:
            dirpath = os.path.join(common.KS_LETTERS_DST_FOLDER, folder)
            if os.path.isdir(dirpath) is False:
                continue
            numimgs = len(os.listdir(dirpath))
            if numimgs < minnum:
                minnum = numimgs
                minfolder = folder
        least = list(filter(lambda a: a["CAPTCHA"].find(minfolder) >= 0, rows))
        if len(least) > common.KS_NUM_CAPTCHAS_ADD:
            least = least[:common.KS_NUM_CAPTCHAS_ADD]
        least = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", least))
        return least

def unknown_lowest_average():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        rows = sorted(rows, key=lambda a: a["AVG"])
        rows = sorted(rows, key=lambda a: a["CORRECT"])
        incorrect = rows[:common.KS_NUM_CAPTCHAS_ADD]
        incorrect = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", incorrect))
        return incorrect

def unknown_random():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        shuffle(rows)
        rows = sorted(rows, key=lambda a: a["CORRECT"])
        rand = rows[:common.KS_NUM_CAPTCHAS_ADD]
        rand = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", rand))
        return rand
