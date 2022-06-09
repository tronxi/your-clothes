from fileinput import filename
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Flatten, Dropout, Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import datetime
import os

class MyCustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_begin(self, batch, logs=None):
        lastBatch = batch - 2
        filename = "/Users/tronxi/workspace/yourClothesMulti/save_at_" + str(lastBatch) + ".h5"
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print(filename, "no existe")
    
    def on_epoch_end(self, batch, logs=None):
        lastBatch = batch - 2
        filename = "/Users/tronxi/workspace/yourClothesMulti/save_at_" + str(lastBatch) + ".h5"
        if os.path.exists(filename):
            os.remove(filename)
    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'vocab_size': self.vocab_size,
            'num_layers': self.num_layers,
            'units': self.units,
            'd_model': self.d_model,
            'num_heads': self.num_heads,
            'dropout': self.dropout,
        })
        return config

image_size = (60, 80)
df = pd.read_csv('archive/styles.csv',error_bad_lines=False)

df.head()
df = df.dropna()
df.nunique()
df.columns

cat_columns = ['articleType','baseColour', 'season']


for colum in cat_columns:
    value_counts = df[colum].value_counts()

    indexes = value_counts.index

    values = value_counts.values

    for i in range(len(value_counts)):

        if values[i] <1000:
            break

    uses = indexes[:i]
    df = df[df[colum].isin(uses)]

data = []
IX = 80
IY = 60
invalid_ids = []
for name in df.id:

    try:
        # img = keras.preprocessing.image.load_img(
        #                     'archive/images/'+str(name)+'.jpg', target_size=image_size
        #                 )
        # img_array = keras.preprocessing.image.img_to_array(img)
        # img_array = tf.expand_dims(img_array, 0)
        image = cv2.imread('archive/images/'+str(name)+'.jpg')
        image = cv2.resize(image, (IX,IY) )
        image = img_to_array(image)
        data.append(image)        
    except: 
        invalid_ids.append(name)

labels = []


for index, row in df.iterrows():

    if row['id'] in invalid_ids:
        continue

    tags = []

    for col in cat_columns:
        tags.append(row[col])

    labels.append(tags)



data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

mlb = MultiLabelBinarizer()
labels = mlb.fit_transform(labels)

print(mlb.classes_)
print(labels[0])

(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.1, random_state=42)


data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
    ]
)
def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    x = data_augmentation(inputs)

    # Entry block
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

model = make_model(input_shape = (IY, IX, 3), num_classes=21)
keras.utils.plot_model(model, show_shapes=True)

E = 9000

callbacks = [
    keras.callbacks.ModelCheckpoint("/Users/tronxi/workspace/yourClothesMulti/save_at_{epoch}.h5"),
    MyCustomCallback()
]
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['mse', 'accuracy'])
model.fit(
    x=trainX,
    y=trainY,
    epochs=E,
    verbose=1,
    callbacks=callbacks)
