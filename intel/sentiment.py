import emoji

def extract_emojis(text):
    print(text)
    emo_list = []
    emo_object = emoji.emoji_list(text)
    for emo in emo_object:
        if emo["emoji"] is not None:
            emo_list.append(emo["emoji"])
    print(emo_list)
    return emo_list
