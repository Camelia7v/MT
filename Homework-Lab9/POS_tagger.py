import spacy
from spacy.lang.ro.examples import sentences
# python -m spacy download ro_core_news_sm


nlp = spacy.load("ro_core_news_sm")
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_)
