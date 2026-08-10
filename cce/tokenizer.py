import string

class Tokenizer:
    def __init__(self):
        # NLTK has been permanently stripped from the engine.
        # The system now uses Geometric Grammar to derive parts of speech autonomously.
        pass
        
    def tokenize(self, text):
        # Maps raw text to semantic nodes (pure topological vertices)
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = clean_text.split()
        
        # Remove duplicates while preserving order
        unique_words = list(dict.fromkeys(words))
        
        # Since we stripped NLTK, we just return the raw words. 
        # The GraphBuilder will query the MetaProcessor's topology for their geometric scalar.
        return [(word, "UNKNOWN") for word in unique_words]
