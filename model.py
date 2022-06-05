import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Flatten, Dropout, Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint


df = pd.read_csv('archive/styles.csv',error_bad_lines=False)

df.head()
df = df.dropna()
df.nunique()
df.columns

cat_columns = ['gender', 'articleType','baseColour', 'season', 'usage']


for colum in cat_columns:
    value_counts = df[colum].value_counts()

    indexes = value_counts.index

    values = value_counts.values

    for i in range(len(value_counts)):

        if values[i] <500:
            break

    uses = indexes[:i]
    df = df[df[colum].isin(uses)]

data = []

IX = 80
IY = 60

invalid_ids = []
for name in df.id:

    try:
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

inputShape = (IY, IX, 3)


model = Sequential()

model.add(Conv2D(32, (3, 3), padding="same",input_shape=inputShape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten()) 

model.add(Dense(128))
model.add(Activation('sigmoid'))


out = len(mlb.classes_)

model.add(Dense(out))
model.add(Activation('sigmoid'))
                    
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['mse', 'accuracy'])

(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.1, random_state=42)

batch = 32
E = 50
callbacks = [
    ModelCheckpoint("save_at_{epoch}.h5"),
]

model.fit(
    x=trainX,
    y=trainY,
    epochs=E,
    verbose=1,
    callbacks=callbacks)