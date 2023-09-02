from model.user import get_user
from model.notes import create_note
from intel.meta_prompt import meta_prompt
from intel.keywords import extract_keywords

def make_note(note_content):
    user = get_user()
    keywords = extract_keywords(note_content)
    note = meta_prompt(note_content, user, "make_note")
    create_note(note, keywords)

    

