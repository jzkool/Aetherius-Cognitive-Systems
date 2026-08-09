import string
import nltk

class Tokenizer:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            print("[Tokenizer] Downloading NLTK POS tagging modules...")
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        
    def tokenize(self, text):
        # Maps raw text to semantic nodes, preserving POS tags for Linguism
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = clean_text.split()
        
        # Remove duplicates while preserving order
        unique_words = list(dict.fromkeys(words))
        
        # Apply Parts of Speech (POS) Tagging
        pos_tagged_tokens = nltk.pos_tag(unique_words)
        return pos_tagged_tokens # Returns list of (word, pos_tag)
