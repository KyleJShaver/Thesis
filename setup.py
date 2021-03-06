# Import project files
import captcha
import isolate_letters
import train
import solve
import common
import reset

import approaches

import os
import sys
import datetime
import multiprocessing
from subprocess import list2cmdline, Popen
from platform import system
import uuid
import json
# import shutil shutil.rmtree()



def parallelcaptchas(num, folder):
    if os.path.exists(folder):
        print("folder {} already exists".format(folder))
    else:
        os.makedirs(folder)
        numgenerate = int(num / multiprocessing.cpu_count())
        diff = num - (numgenerate * multiprocessing.cpu_count())
        processes = []
        started = 0
        while True:
            while len(processes) < multiprocessing.cpu_count() and started < multiprocessing.cpu_count():
                pythoncall = "python"
                if __name__ == "__main__" and len(sys.argv) > 1:
                    pythoncall = sys.argv[1]
                task = [pythoncall, "captcha.py", "{}".format(numgenerate + diff), folder]
                diff -= diff
                cmd = list2cmdline(task)
                if system() == "Windows":
                    processes.append(Popen(cmd))
                else:
                    processes.append(Popen(cmd, shell=True))
                started += 1
            for p in processes:
                if p.poll() is not None:
                    if p.returncode == 0:
                        processes.remove(p)
                        p.kill()
                    else:
                        sys.exit(1)
            if not processes:
                break
        print("{} Done generating {} captchas in {}\n\n".format(datetime.datetime.now() - start, num, folder))

def runapproach(addcaptchas, folder, letters, model, label, output):
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.makedirs(letters)
        isolate_letters.isolateletters(common.KS_CAPTCHA_SOLVE_FOLDER, letters, addcaptchas)
        train.train(common.KS_LETTERS_DST_FOLDER, model, label, letters, common.KS_MODEL_FILE)
        solve.solve(model, label, common.KS_CAPTCHA_IMMUT_FOLDER, output)
    common.compareimmut(output)

def runapproachprops(addcaptchas, props):
    runapproach(addcaptchas, props["folder"], props["letters"], props["model"], props["labels"], props["immut"])

while True:
    reset.reset()
    start = datetime.datetime.now()
    UUID = str(uuid.uuid4())
    results_files = dict()
    results_files["baseline"] = common.KS_IMMUT_BASELINE

    # --------------------
    # ------ STEP 1 ------
    # --------------------

    print("\nGenerating CAPTCHAs...\n")

    # Generate captchas to train the system
    parallelcaptchas(common.KS_CAPTCHA_TRAIN_NUM, common.KS_CAPTCHA_TRAIN_FOLDER)

    # Generate the captchas to test and determine which ones to use to retrain the model
    parallelcaptchas(common.KS_CAPTCHA_SOLVE_NUM, common.KS_CAPTCHA_SOLVE_FOLDER)

    # Generate an immutable set to analyze performance
    parallelcaptchas(common.KS_CAPTCHA_IMMUT_NUM, common.KS_CAPTCHA_IMMUT_FOLDER)

    # --------------------
    # ------ STEP 2 ------
    # --------------------

    print("\nIsolating letters for the training CAPTCHAs...\n")

    # Isolate the letters in the training captchas
    if os.path.exists(common.KS_LETTERS_DST_FOLDER):
        print("folder {} already exists".format(common.KS_LETTERS_DST_FOLDER))
    else:
        isolate_letters.isolateletters(common.KS_CAPTCHA_TRAIN_FOLDER, common.KS_LETTERS_DST_FOLDER)
        print("{} Done isolating letters from training captchas to {}\n\n".format(datetime.datetime.now() - start, common.KS_CAPTCHA_TRAIN_FOLDER))

    # --------------------
    # ------ STEP 3 ------
    # --------------------

    print("\nTraining model...\n")

    # Train the model
    if os.path.exists(common.KS_MODEL_FILE) and os.path.exists(common.KS_LABEL_FILE):
        print("files {} and {} already exists".format(common.KS_MODEL_FILE, common.KS_LABEL_FILE))
    else:
        train.train(common.KS_LETTERS_DST_FOLDER, common.KS_MODEL_FILE, common.KS_LABEL_FILE)
        print("{} Done training model to {}\n\n".format(datetime.datetime.now() - start, common.KS_MODEL_FILE))

    # --------------------
    # ------ STEP 4 ------
    # --------------------

    print("\nSolving CAPTHAs...\n")

    # Get baseline for capthas_solve
    if os.path.exists(common.KS_SOLVE_BASELINE):
        print("file {} already exists".format(common.KS_SOLVE_BASELINE))
    else:
        solve.solve(common.KS_MODEL_FILE, common.KS_LABEL_FILE, common.KS_CAPTCHA_SOLVE_FOLDER, common.KS_SOLVE_BASELINE)
        print("{} Done solving for CAPTCHAs in {} and saved to {}".format(datetime.datetime.now() - start, common.KS_CAPTCHA_SOLVE_FOLDER, common.KS_SOLVE_BASELINE))

    # Get baseline for capthas_immut
    if os.path.exists(common.KS_IMMUT_BASELINE):
        print("file {} already exists".format(common.KS_IMMUT_BASELINE))
    else:
        solve.solve(common.KS_MODEL_FILE, common.KS_LABEL_FILE, common.KS_CAPTCHA_IMMUT_FOLDER, common.KS_IMMUT_BASELINE)
        print("{} Done solving for CAPTCHAs in {} and saved to {}".format(datetime.datetime.now() - start, common.KS_CAPTCHA_IMMUT_FOLDER, common.KS_IMMUT_BASELINE))

    # --------------------
    # ------ STEP 5 ------
    # --------------------

    print("\nRunning approaches...\n")
    # Run random
    props = approaches.getprops(common.KS_APP_RANDOM_FOLDER)
    results_files["random"] = props["immut"]
    addcaptchas = approaches.random()
    runapproachprops(addcaptchas, props)

    # Run lowest average confidence
    props = approaches.getprops(common.KS_APP_LOWEST_AVG_FOLDER)
    results_files["lowest_average"] = props["immut"]
    addcaptchas = approaches.lowest_average()
    runapproachprops(addcaptchas, props)

    # Run lowest letter confidence
    props = approaches.getprops(common.KS_APP_LOWEST_LETTER_FOLDER)
    results_files["lowest_letter_confidence"] = props["immut"]
    addcaptchas = approaches.lowest_letter()
    runapproachprops(addcaptchas, props)

    # Run least represented letter
    props = approaches.getprops(common.KS_APP_LEAST_REP_FOLDER)
    results_files["least_represented_letter"] = props["immut"]
    addcaptchas = approaches.least_rep()
    runapproachprops(addcaptchas, props)

    # Run unknown (priority given to lowest average)
    props = approaches.getprops(common.KS_APP_UNKNOWN_LOWEST_AVG_FOLDER)
    results_files["unknown_lowest_average"] = props["immut"]
    addcaptchas = approaches.unknown_lowest_average()
    runapproachprops(addcaptchas, props)

    # Run unknown (random priority)
    props = approaches.getprops(common.KS_APP_UNKNOWN_RANDOM_FOLDER)
    results_files["unknown_random"] = props["immut"]
    addcaptchas = approaches.unknown_random()
    runapproachprops(addcaptchas, props)

    # Run unknown (priority to lowest letter confidence)
    props = approaches.getprops(common.KS_APP_UNKNOWN_LOWEST_LETTER_FOLDER)
    results_files["unknown_lowest_letter"] = props["immut"]
    addcaptchas = approaches.unknown_lowest_letter()
    runapproachprops(addcaptchas, props)

    print("{} Done running all approaches".format(datetime.datetime.now() - start))

    end = datetime.datetime.now()
    post_data = dict()
    for approach, file in results_files.items():
        post_data[approach] = common.analyzefile(file)
    post_data["uuid"] = UUID
    post_data["time"] = str(end)
    common.sendtofirebase(sys.argv[2], post_data)

    print("Total runtime was: {}".format(end - start))