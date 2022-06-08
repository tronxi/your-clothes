import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_core_news_sm")

text = "Hola me llaman Sergio y tengo un Mac y vivo en madrid"
text = "Hola su nombre es Irene, mi amigo se llama Sergio y yo soy Pablo"
doc = nlp(
    text
)
# for token in doc:
#     print(token.text, token.pos_)

# for ent in doc.ents:
#     print(ent.text, ent.label_)

print(doc.text)
matcher = Matcher(nlp.vocab)
namePatterns = [
    [{"LEMMA": "llamar"} ,{"POS": "PROPN"}],
    [{"LEMMA": "nombre"}, {"POS": "AUX", "OP": "?"},{"POS": "PROPN"}],
    [{"TEXT": "soy"}, {"POS": "PROPN"}],
]

matcher.add("namePatterns", namePatterns)
matches = matcher(doc)

if len(matches) == 0:
    print("no te he entendido")
else:
    for match_id, start, end in matches:
        matched_span = doc[start:end]
        # print("Encontrado", matched_span.text)
        for token in matched_span:
            if token.pos_ == "PROPN":
                print("hola", token.text)