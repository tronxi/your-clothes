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
            [{"LEMMA": "nombre"}, {"POS": "AUX", "OP": "?"},{"POS": "PROPN"}],
            [{"TEXT": "soy"}, {"POS": "PROPN"}],
            [{"POS": "NOUN"}],
            [{"POS": "PROPN"}],
        ]
        self.colorPatterns = [
            [{"LEMMA": "color"}, {"POS": "ADJ"}],
            [{"LEMMA": "ropa"}, {"POS": "ADJ"}],
            [{"TEXT": {"IN": ["mochila", "cinturon", "ropa interior", "zapatillas", "zapatos", "vaqueros", "sandalias", "camisa", "pantalones cortos", "calcetines", "deportivas", "gafas", "top", "camiseta", "reloj", "pantalones"]}}, {"POS": "ADJ"}],
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
            [{"TEXT": {"IN": ["mochila", "cinturon", "ropa interior", "zapatillas", "zapatos", "vaqueros", "sandalias", "camisa", "pantalones cortos", "calcetines", "deportivas", "gafas", "top", "camiseta", "reloj", "pantalones"]}}]
        ]

        self.deleteColor = [
            [{"LEMMA": "borrar"}, {"ORTH": "el"}, {"ORTH": "color"}],
            [{"LEMMA": "cambiar"}, {"ORTH": "el"}, {"ORTH": "color"}],
            [{"LEMMA": "eliminar"}, {"ORTH": "el"}, {"ORTH": "color"}],
            [{"LEMMA": "borrar"}, {"ORTH": "color"}],
            [{"LEMMA": "cambiar"}, {"ORTH": "color"}],
            [{"LEMMA": "eliminar"}, {"ORTH": "color"}],
        ]

        self.deleteType = [
            [{"LEMMA": "borrar"}, {"ORTH": "el"}, {"ORTH": "tipo"}],
            [{"LEMMA": "cambiar"}, {"ORTH": "el"}, {"ORTH": "tipo"}],
            [{"LEMMA": "eliminar"}, {"ORTH": "el"}, {"ORTH": "tipo"}],
            [{"LEMMA": "borrar"}, {"ORTH": "tipo"}],
            [{"LEMMA": "cambiar"}, {"ORTH": "tipo"}],
            [{"LEMMA": "eliminar"}, {"ORTH": "tipo"}],
        ]

        self.deleteSeason = [
            [{"LEMMA": "borrar"}, {"ORTH": "la"}, {"ORTH": "temporada"}],
            [{"LEMMA": "cambiar"}, {"ORTH": "la"}, {"ORTH": "temporada"}],
            [{"LEMMA": "eliminar"}, {"ORTH": "la"}, {"ORTH": "temporada"}],
            [{"LEMMA": "borrar"}, {"ORTH": "temporada"}],
            [{"LEMMA": "cambiar"}, {"ORTH": "temporada"}],
            [{"LEMMA": "eliminar"}, {"ORTH": "temporada"}],
        ]

    def response(self, text):
        doc = self.nlp(text)
        self.new = False
        self.recommender = False
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
                self.message = "no te he entendido, puedes repetirlo?"
            else:
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    for token in matched_span:
                        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
                            self.message = "hola " + token.text + ", en que puedo ayudarte?"
                            self.name = token.text
        else:
            found = False
            deleted = False

            matcher = Matcher(self.nlp.vocab)
            matcher.add("newPatterns", self.newPatterns)
            matches = matcher(doc)
            for _, start, end in matches:
                matched_span = doc[start:end]
                found = True
                self.new =True
                self.recommender = True
            
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
                            self.recommender = True
                
                matcher = Matcher(self.nlp.vocab)
                matcher.add("seasonPatterns", self.seasonPatterns)
                matches = matcher(doc)
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    found = True
                    self.season = matched_span.text
                    self.recommender = True

                matcher = Matcher(self.nlp.vocab)
                matcher.add("typePatterns", self.typePatterns)
                matches = matcher(doc)
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    found = True
                    self.type = matched_span.text
                    self.recommender = True

                matcher = Matcher(self.nlp.vocab)
                matcher.add("deleteColor", self.deleteColor)
                matches = matcher(doc)
                for _, start, end in matches:
                    found = True
                    deleted = True
                    self.color = ""
                    self.recommender = True
                
                matcher = Matcher(self.nlp.vocab)
                matcher.add("deleteType", self.deleteType)
                matches = matcher(doc)
                for _, start, end in matches:
                    found = True
                    deleted = True
                    self.type = ""
                    self.recommender = True

                matcher = Matcher(self.nlp.vocab)
                matcher.add("deleteSeason", self.deleteSeason)
                matches = matcher(doc)
                for _, start, end in matches:
                    found = True
                    deleted = True
                    self.season = ""
                    self.recommender = True
                
            if not found:
                self.message = "no te he entendido, puedes repetirlo?"
            elif self.new:
                self.message = "genial, vuelvo a clasificar tu ropa"
            elif deleted:
                self.message = "vale, borro ese elemento, en que más puedo ayudarte?"
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


