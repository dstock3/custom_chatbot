import emoji

def extract_emojis(text):
    emo_list = []
    emo_object = emoji.emoji_list(text)
    for emo in emo_object:
        if emo["emoji"] is not None:
            emo_list.append(emo["emoji"])
    
    cleaned_text = ''.join([c for c in text if c not in emo_list])
    
    return emo_list, cleaned_text