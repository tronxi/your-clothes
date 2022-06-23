from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
import spacy
import csv

class RecomendadorAgent(Agent):
    class RecomendadorBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=90000)
            if msg:
                caracteristicas = msg.body.split(",")
                color = caracteristicas[0]
                season = caracteristicas[1]
                type = caracteristicas[2]

                doc = self.nlp(color)
                for token in doc:
                    color = self.colorDict.get(token.lemma_, "")

                doc = self.nlp(season)
                for token in doc:
                    season = self.seasonDict.get(token.lemma_, "")

                type = self.typeDict.get(type, "")
                # print("recomendador - ", "color: ", color, ", season: ", season, ", type: ", type)
                with open("./armario.csv") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line = 0
                    total_matches = 0
                    photos = []
                    for row in csv_reader:
                        if line == 0:
                            line += 1
                        else:
                            matches = 0
                            if color == "" or color == row[1]:
                                matches += 1
                            if season == "" or season == row[2]:
                                matches += 1
                            if type == "" or type == row[3]:
                                matches += 1
                            if matches == 3:
                                total_matches += 1
                                photos.append(row[0])
                    if total_matches == 0:
                        print("Lo siento no he encontrado ningun articulo con esas caracteristicas")
                    else:
                        print("He encontrado los siguientes articulos con esas caracteristicas:")
                        for photo in photos:
                            print(photo)
        
        async def on_start(self):
            self.nlp = spacy.load("es_core_news_sm")
            self.seasonDict = {
                "primavera": "Spring",
                "verano": "Summer",
                "otoño": "Fall",
                "invierno": "Winter",
                "calor": "Summer",
                "frio": "Winter"
            }

            self.colorDict = {
                "beis": "Beige",
                "negro": "Black",
                "azul": "Blue",
                "marrón": "Brown",
                "dorado": "Gold",
                "verde": "Green",
                "gris": "Grey",
                "granate": "Maroon",
                "azul marino": "Navy Blue",
                "narnaja": "Orange",
                "narnajar": "r",
                "rosa": "Pink",
                "morada": "Purple",
                "morado": "Purple",
                "rojo": "Red",
                "plateado": "Silver",
                "blanco": "White",
                "amarillo": "Yellow"
            }

            self.typeDict = {
                "mochila": "Backpacks", 
                "cinturon": "Belts", 
                "ropa interior": "Briefs", 
                "zapatillas": "Casual Shoes", 
                "zapatos": "Formal Shoes", 
                "vaqueros": "Jeans",
                "sandalias": "Sandals", 
                "camisa": "Shirts", 
                "pantalones cortos": "Shorts", 
                "calcetines": "Socks", 
                "deportivas": "Sport Shoes", 
                "gafas": "Sunglasses", 
                "top": "Tops", 
                "camiseta": "Tshirts", 
                "reloj": "Watches", 
                "pantalones": "Trousers"
            }
                
    async def setup(self):
        b = self.RecomendadorBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)