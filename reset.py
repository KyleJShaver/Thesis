import os
import shutil
import common

shutil.rmtree(common.KS_CAPTCHA_TRAIN_FOLDER, True)
shutil.rmtree(common.KS_CAPTCHA_SOLVE_FOLDER, True)
shutil.rmtree(common.KS_CAPTCHA_IMMUT_FOLDER, True)
shutil.rmtree(common.KS_LETTERS_DST_FOLDER, True)
os.unlink(common.KS_MODEL_FILE)
os.unlink(common.KS_LABEL_FILE)
os.unlink(common.KS_SOLVE_BASELINE)
os.unlink(common.KS_IMMUT_BASELINE)
#os.unlink(common.)

shutil.rmtree(common.KS_APP_LOWEST_AVG_FOLDER, True)
shutil.rmtree(common.KS_APP_RANDOM_FOLDER, True)
shutil.rmtree(common.KS_APP_LOWEST_LETTER_FOLDER, True)
shutil.rmtree(common.KS_APP_LEAST_REP_FOLDER, True)
#shutil.rmtree(common.)