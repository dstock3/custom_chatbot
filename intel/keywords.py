import spacy
nlp = spacy.load('en_core_web_lg')

def extract_keywords(text):
    doc = nlp(text)
    
    keywords = set()
    
    for ent in doc.ents:
        if ent.label_ in ('PERSON', 'ORG', 'GPE', 'FAC', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART'):
            keywords.add(ent.text)

    for token in doc:
        if token.pos_ in ('NOUN', 'PROPN'):
            keywords.add(token.text)

        if token.ent_type_ == 0:
            keywords.add(token.lemma_)
    return list(keywords)