class Tokenizer:
    def __init__(self):
        pass
        
    def tokenize(self, text):
        # Maps raw text to semantic nodes
        words = text.lower().replace(',', '').replace('.', '').split()
        return list(dict.fromkeys(words)) # unique concepts
