from urllib import response
import spacy
from spacy.matcher import Matcher

class Bot:
    def __init__(self):
        self.name = ""
        self.color = ""
        self.season = ""
        self.type = ""
        self.new = False
        self.recommender = False
        self.message = ""
        self.nlp = spacy.load("es_core_news_sm")
        self.namePatterns = [
            [{"LEMMA": "llamar"} ,{"POS": "PROPN"}],
            # [{"LEMMA": "nombre"}, {"POS": "AUX", "OP": "?"},{"POS": "PROPN"}],
            [{"TEXT": "soy"}, {"POS": "PROPN"}],
            [{"POS": "NOUN"}],
        ]
        self.colorPatterns = [
            [{"LEMMA": "color"}, {"POS": "ADJ"}],
            [{"LEMMA": "ropa"}, {"POS": "ADJ"}],
            [{"TEXT": {"IN": ["mochila", "cinturon", "ropa interior", "zapatillas", "zapatos", "vaqueros", "vaqueros", "sandalias", "camisa", "pantalones cortos", "calcetines", "zapatillas de deporte", "gafas", "top", "camiseta", "reloj", "pantalones"]}}, {"POS": "ADJ"}],
            [{"TEXT": {"IN": ["primavera", "verano", "otoño", "invierno", "calor", "frio"]}}, {"POS": "ADJ"}]
        ]

        self.seasonPatterns = [
            [{"TEXT": {"IN": ["primavera", "verano", "otoño", "invierno", "calor", "frio"]}}]
        ]

        self.newPatterns = [
            [{"LEMMA": "nuevo"}],
            [{"LEMMA": "comprar"}],
            [{"LEMMA": "añadir"}],
        ]

        self.typePatterns = [
            [{"TEXT": {"IN": ["mochila", "cinturon", "ropa interior", "zapatillas", "zapatos", "vaqueros", "vaqueros", "sandalias", "camisa", "pantalones cortos", "calcetines", "zapatillas de deporte", "gafas", "top", "camiseta", "reloj", "pantalones"]}}]
        ]

    def response(self, text):
        doc = self.nlp(text)
        self.new = False
        self.recommender = True
        self.message = ""
        # print("####")
        # for token in doc:
        #     print(token.text, token.pos_)
        # print("####")

        if self.name == "":
            matcher = Matcher(self.nlp.vocab)
            matcher.add("namePatterns", self.namePatterns)
            matches = matcher(doc)
            if len(matches) == 0:
                return "no te he entendido, puedes repetirlo?"
            else:
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    for token in matched_span:
                        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
                            self.message += "hola " + token.text + ", en que puedo ayudarte?"
                            self.name = token.text
        else:
            found = False

            matcher = Matcher(self.nlp.vocab)
            matcher.add("newPatterns", self.newPatterns)
            matches = matcher(doc)
            for _, start, end in matches:
                matched_span = doc[start:end]
                found = True
                self.new =True
            
            if not found:
                matcher = Matcher(self.nlp.vocab)
                matcher.add("colorPatterns", self.colorPatterns)
                matches = matcher(doc)
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    for token in matched_span:
                        if token.pos_ == "ADJ":
                            self.color = token.text
                            found = True
                
                matcher = Matcher(self.nlp.vocab)
                matcher.add("seasonPatterns", self.seasonPatterns)
                matches = matcher(doc)
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    found = True
                    self.season = matched_span.text

                matcher = Matcher(self.nlp.vocab)
                matcher.add("typePatterns", self.typePatterns)
                matches = matcher(doc)
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    found = True
                    self.type = matched_span.text
                
                matcher = Matcher(self.nlp.vocab)
                matcher.add("newPatterns", self.newPatterns)
                matches = matcher(doc)
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    found = True
                    self.new =True
                
            if not found:
                self.message = "no te he entendido, puedes repetirlo?"
            elif self.new:
                self.message = "genial, vuelvo a clasificar tu ropa"
            else:
                self.message = self._generateMessage()
        return self.message, self.name, self.color, self.season, self.type, self.new, self.recommender

    def _generateMessage(self):
        message = "Vale, busco ropa"
        if self.type != "":
            message += " tipo " + self.type
        if self.color != "":
            message += " color " + self.color
        if self.season != "":
            message += " temporada " + self.season
        return message


