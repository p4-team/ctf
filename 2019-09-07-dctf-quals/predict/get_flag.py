import numpy as np
import binascii
from keras import *
from keras.layers import *

from keras.callbacks import ModelCheckpoint, Callback
from PIL import Image
import keras

x_train = np.load("X.npy")
y_train = np.load("y.npy")

flag = np.load("flag.npy")


print(x_train)
print(x_train.shape)
print(y_train.shape)
print(flag.shape)

img = Image.fromarray(flag[0], 'RGB')
#img.save('my.png')
#img.show()

flag = flag.astype('float32')
flag /= 255

batch_size = 128
num_classes = 2
epochs = 24

# input image dimensions
img_rows, img_cols = 50, 50


input_shape = (img_rows, img_cols, 3)

x_train = x_train.astype('float32')
x_train /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

filepath="weights-improvement-{epoch:02d}-{loss:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=False, mode='max')
class CheckFlag(Callback):
    def __init__(self):
        super(CheckFlag, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        out = model.predict(flag)
        z = []
        for a in out:
            z.append(np.argmax(a))
        o = "".join([str(int(x)) for x in z])
        l = hex(int(o, 2)).replace("L","").replace("l","")[2:]
        print(l)
        f = binascii.unhexlify(l)
        print(f)
        o = "".join([str(1-int(x)) for x in z])
        l = hex(int(o, 2)).replace("L","").replace("l","")[2:]
        print(l)
        f = binascii.unhexlify(l)
        print(f)


callbacks_list = [checkpoint, CheckFlag()]

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          callbacks=callbacks_list,
          epochs=epochs,
          verbose=1)

out = model.predict(flag)
print(np.argmax(out))
print(out)

