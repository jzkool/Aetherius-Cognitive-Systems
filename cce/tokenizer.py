import string

class Tokenizer:
    def __init__(self):
        pass
        
    def tokenize(self, text):
        # Maps raw text to semantic nodes, stripping all punctuation
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = clean_text.split()
        return list(dict.fromkeys(words)) # unique concepts
