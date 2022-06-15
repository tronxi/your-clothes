import spacy
from spacy.matcher import Matcher

class Bot:
    def __init__(self):
        self.name = ""
        self.color = ""
        self.nlp = spacy.load("es_core_news_sm")
        self.namePatterns = [
            [{"LEMMA": "llamar"} ,{"POS": "PROPN"}],
            # [{"LEMMA": "nombre"}, {"POS": "AUX", "OP": "?"},{"POS": "PROPN"}],
            [{"TEXT": "soy"}, {"POS": "PROPN"}],
            [{"POS": "NOUN"}],
        ]
        self.colorPatterns = [
            [{"LEMMA": "color"}, {"POS": "ADJ"}],
            [{"LEMMA": "ropa"}, {"POS": "ADJ"}]
        ]

        self.recommenderPatterns = [
            [{"LEMMA": "recomendar"}],
            [{"LEMMA": "recomendacion"}],
            [{"LEMMA": "recomiendo"}],
        ]

    def response(self, text):
        doc = self.nlp(text)

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
                message = ""
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    for token in matched_span:
                        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
                            message += "hola " + token.text + ", en que puedo ayudarte?"
                            self.name = token.text
            return message, False
        else:
            found = False
            recommender = False
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
            matcher.add("recommenderPatterns", self.recommenderPatterns)
            matches = matcher(doc)
            for _, start, end in matches:
                matched_span = doc[start:end]
                found = True
                recommender = True
            if not found:
                return "no te he entendido, puedes repetirlo?", False
            else:
                return self.color, recommender

