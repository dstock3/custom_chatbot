import spacy
from model.user import get_user
nlp = spacy.load('en_core_web_lg')

def extract_keywords(text):
    user = get_user()

    username = user['name']
    system_name = user['system_name']

    doc = nlp(text)
    
    keywords = set()
    
    for ent in doc.ents:
        if ent.label_ in ('PERSON', 'ORG', 'GPE', 'FAC', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART') and len(ent.text) > 1:
            keywords.add(ent.text)

    for token in doc:
        if token.pos_ in ('NOUN', 'PROPN') and len(token.text) > 1:
            keywords.add(token.text)

        if token.ent_type_ == 0 and len(token.lemma_) > 1:
            keywords.add(token.lemma_)

    #remove username and system name from keywords
    if username in keywords:
        keywords.remove(username)
    if system_name in keywords:
        keywords.remove(system_name)
    return list(keywords)