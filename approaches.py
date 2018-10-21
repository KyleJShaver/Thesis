import common

import csv
import os
from random import shuffle

def random():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        rows = shuffle(rows)
        lowest = rows[:common.KS_NUM_CAPTCHAS_ADD]
        lowest = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", lowest))
        return lowest

def lowest_average():
    with open(common.KS_SOLVE_BASELINE) as solvebase:
        reader = csv.DictReader(solvebase)
        rows = []
        for row in reader:
            rows.append(row)
        rows = sorted(rows, key=lambda a : a["AVG"])
        lowest = rows[:common.KS_NUM_CAPTCHAS_ADD]
        lowest = list(map(lambda a: os.path.join(common.KS_CAPTCHA_SOLVE_FOLDER, a["CAPTCHA"]) + ".png", lowest))
        return lowest
