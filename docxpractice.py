import spacy
nlp=spacy.load("en_core_web_sm")
text = "Apple is looking at buying a U.K. startup for $1 billion near London by January 2027."
doc=nlp(text)
print(doc.ents)