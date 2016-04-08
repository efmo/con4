from __future__ import print_function
from algoplayer import ConnectFourGame
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from numpy import asarray
import c4generator as c4g
import random

NUM_ROWS = 6
NUM_COLS = 7
batch_size = 32
nb_classes = 3 # red win, blue win, tie
nb_epoch = 20

labels = c4g.recordGamesDupeLimit(1000, 20)
teDex = random.sample(xrange(len(labels)), len(labels)/8)
test = [labels[i] for i in teDex]
train = [labels[i] for i in xrange(len(labels)) if i not in teDex]
trX, trY = map(list, zip(*train))
teX, teY = map(list, zip(*test))

trY = [[1, 0] if x == 1 else [0, 1] for x in trY]
teY = [[1, 0] if x == 1 else [0, 1] for x in teY]

trX = asarray(trX)
teX = asarray(teX)
trX = trX.reshape(trX.shape[0], 1, NUM_ROWS, NUM_COLS)
teX = teX.reshape(teX.shape[0], 1, NUM_ROWS, NUM_COLS)

trY = asarray(trY)
teY = asarray(teY)

model = Sequential()

model.add(Convolution2D(32, 3, 3, border_mode='same',
                        input_shape=(1, NUM_ROWS, NUM_COLS)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(2)) # Either red or blue.
model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

con4 = ConnectFourGame()
con4.evalModel(model)
model.fit(trX, trY, batch_size=batch_size,
          nb_epoch=nb_epoch, show_accuracy=True,
          validation_data=(teX, teY), shuffle=True)
con4.evalModel(model)