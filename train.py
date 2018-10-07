# STEP 3: Train the model
import imutils
from imutils import paths
import os.path
import cv2
import numpy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
import pickle
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from captcha import usedglyphs

src_folder = "letters"
model_savefile = "model.hdf5"
model_labelfile = "labels.dat"
image_size = 20

data = []
labels = []

for imgfile in paths.list_images(src_folder):
    image = cv2.imread(imgfile)
    if image is None:
        print(imgfile + " is empty")
        continue
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (h, w) = image.shape[:2]
    pad = (image_size - min(h, w)) / 2.0
    if pad % 1 is not 0:
        pad = pad % 1
    pad = int(pad)
    white = [255, 255, 255]
    if w > h:
        image = imutils.resize(image, width=image_size)
        image = cv2.copyMakeBorder(image, pad, pad, 0, 0, cv2.BORDER_CONSTANT, value=white)
    else:
        image = imutils.resize(image, height=image_size)
        image = cv2.copyMakeBorder(image, 0, 0, pad, pad, cv2.BORDER_CONSTANT, value=white)
    image = cv2.resize(image, (image_size, image_size))
    image = numpy.expand_dims(image, axis=2)
    label = imgfile.split(os.path.sep)[-2]
    data.append(image)
    labels.append(label)

data = numpy.array(data, dtype="float") / 255.0
labels = numpy.array(labels)

(trnx, tstx, trny, tsty) = train_test_split(data, labels, test_size=0.25, random_state=0)
lb = LabelBinarizer().fit(trny)
trny = lb.transform(trny)
tsty = lb.transform(tsty)

with open(model_labelfile, "wb") as labelfile:
    pickle.dump(lb, labelfile)

model = Sequential()
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Hidden layer with 500 nodes
model.add(Flatten())
model.add(Dense(500, activation="relu"))

# Output layer with 36 nodes (one for each possible letter/number we predict)
model.add(Dense(len(usedglyphs()), activation="softmax"))

# Ask Keras to build the TensorFlow model behind the scenes
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(trnx, trny, validation_data=(tstx, tsty), epochs=10, verbose=1)

model.save(model_savefile)
