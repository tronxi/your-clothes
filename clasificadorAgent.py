from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from keras.models import load_model
import glob
import csv
import tensorflow as tf
from tensorflow import keras

class ClasificadorAgent(Agent):
    class ClasificadorBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=90000)
            if msg:

                image_size = (400, 533)

                with open('./armario.csv', 'w', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    header = ['image', 'color', 'season', 'type']
                    writer.writerow(header)
                    for image in glob.glob("./armario/*"):
                        imageList = []
                        imageList.append(image)
                        print(image)
                        img = keras.preprocessing.image.load_img(
                            image, target_size=image_size
                        )
                        img_array = keras.preprocessing.image.img_to_array(img)
                        img_array = tf.expand_dims(img_array, 0)

                        predictions = self.colorModel.predict(img_array)
                        cl = predictions.argmax(axis=-1)[0]
                        imageList.append(self.colorClasses[cl])

                        predictions = self.seasonModel.predict(img_array)
                        cl = predictions.argmax(axis=-1)[0]
                        imageList.append(self.seasonClasses[cl])

                        predictions = self.typeModel.predict(img_array)
                        cl = predictions.argmax(axis=-1)[0]
                        imageList.append(self.typeClasses[cl])

                        writer.writerow(imageList)
        async def on_start(self):
            self.colorModel = load_model('./model/save_at_color_21.h5')
            self.colorClasses = ['Beige', 'Black', 'Blue', 'Brown', 'Gold', 'Green', 'Grey', 'Maroon', 'Navy Blue', 'Orange', 'Pink', 'Purple', 'Red', 'Silver', 'White', 'Yellow']

            self.seasonModel = load_model("./model/save_at_season_24.h5")
            self.seasonClasses = ['Fall', 'Spring', 'Summer', 'Winter']

            self.typeModel = load_model("./model/save_at_type_47.h5")
            self.typeClasses = ['Backpacks', 'Belts', 'Briefs', 'Casual Shoes', 'Formal Shoes', 'Jeans', 'Sandals', 'Shirts', 'Shorts', 'Socks', 'Sports Shoes', 'Sunglasses', 'Tops', 'Trousers', 'Tshirts', 'Watches']

                
    async def setup(self):
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        b = self.ClasificadorBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)