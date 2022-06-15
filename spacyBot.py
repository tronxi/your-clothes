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
            return message
        else:
            matcher = Matcher(self.nlp.vocab)
            matcher.add("colorPatterns", self.colorPatterns)
            matches = matcher(doc)

            if len(matches) == 0:
                return "no te he entendido, puedes repetirlo?"
            else:
                message = ""
                for _, start, end in matches:
                    matched_span = doc[start:end]
                    for token in matched_span:
                        if token.pos_ == "ADJ":
                            message += "Perfecto, ropa de color " + token.text
                            self.color = token.text
            return message

