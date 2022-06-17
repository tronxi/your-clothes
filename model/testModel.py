from keras.models import load_model
from tensorflow import keras
import tensorflow as tf
import glob
import csv

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
labels = ['Black', 'Blue', 'Brown', 'Casual Shoes', 'Fall', 'Green' ,'Grey', 'Handbags',
 'Heels', 'Kurtas', 'Purple', 'Red', 'Shirts', 'Sports Shoes', 'Summer',
 'Sunglasses', 'Tops', 'Tshirts' ,'Watches' ,'White' ,'Winter']

img = keras.preprocessing.image.load_img(
                            "archive/images/50906.jpg", target_size=image_size
                        )
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

model = load_model('/Users/tronxi/workspace/yourClothesMulti/save_at_2.h5', custom_objects={'CustomCallback': MyCustomCallback})
predictions = model.predict(img_array)

num = 0;
for pred in predictions[0]:
    print(labels[num] + ": " + str(pred))
    num += 1