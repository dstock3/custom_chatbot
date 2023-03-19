import string
import emoji

def extract_emojis(s):
    return ''.join(c for c in s if c in string.printable and c in emoji.UNICODE_EMOJI)
