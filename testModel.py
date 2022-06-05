from keras.models import load_model
from tensorflow import keras
import tensorflow as tf
import glob
import csv

image_size = (60, 80)
labels = ['Backpacks', 'Beige', 'Belts', 'Black', 'Blue', 'Boys', 'Briefs', 'Brown',
 'Casual', 'Casual Shoes', 'Ethnic', 'Fall', 'Flats', 'Flip Flops', 'Formal',
 'Formal Shoes', 'Green', 'Grey', 'Handbags', 'Heels', 'Jeans', 'Kurtas', 'Men',
 'Navy Blue', 'Pink', 'Purple', 'Red', 'Sandals', 'Shirts', 'Shorts', 'Silver',
 'Socks', 'Sports' ,'Sports Shoes' ,'Summer' ,'Sunglasses' ,'Tops' ,'Trousers',
 'Tshirts' ,'Unisex', 'Wallets', 'Watches', 'White', 'Winter', 'Women', 'Yellow']

img = keras.preprocessing.image.load_img(
                            "archive/images/22728.jpg", target_size=image_size
                        )
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

model = load_model('save_at_1.h5')
predictions = model.predict(img_array)

num = 0;
for pred in predictions[0]:
    if pred > 0.5:
        print(labels[num] + ": " + str(pred))
    num += 1