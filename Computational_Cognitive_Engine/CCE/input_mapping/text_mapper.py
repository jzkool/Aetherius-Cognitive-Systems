import hashlib
import string
from typing import List, Dict, Set, Iterable

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# IMPORTANT: do not call nltk.download() unconditionally in Spaces.

class TextToChaosMapper:
    def __init__(self, num_shards: int = 1024):
        self.shard_to_word: Dict[int, str] = {}
        self.lemmatizer = WordNetLemmatizer()
        # Use a safe fallback if stopwords are missing
        try:
            self.stop_words = set(stopwords.words("english"))
        except LookupError:
            self.stop_words = set()
        self.num_shards = max(1, int(num_shards))

    def _clean_and_tokenize(self, text: str) -> List[str]:
        """
        NLTK-based tokenization + lemmatization + stopword/punctuation filtering.
        Returns a list of cleaned lemma tokens.
        """
        if not text:
            return []

        text = text.lower()
        raw_tokens = word_tokenize(text)

        cleaned_tokens: List[str] = []
        for t in raw_tokens:
            # Remove punctuation from ends and interior punctuation except caret and dot and underscore
            # (preserve tokens like x^2 or 3.14 if you want numeric tokens)
            t = t.strip(string.punctuation)
            # Remove remaining punctuation characters
            t = t.translate(str.maketrans("", "", string.punctuation))
            if not t:
                continue
            if t in self.stop_words:
                continue
            # Lemmatize; for verbs you could pass pos='v' if you detect verbs
            base_word = self.lemmatizer.lemmatize(t)
            cleaned_tokens.append(base_word)
        return cleaned_tokens

    def _hash_token(self, token: str) -> int:
        """
        Stable hash of a token mapped into [0, num_shards-1].
        Uses SHA256 for determinism across runs and platforms.
        """
        if not token:
            return 0
        h = hashlib.sha256(token.encode("utf-8")).digest()
        # Use first 8 bytes as integer
        val = int.from_bytes(h[:8], "big", signed=False)
        return val % self.num_shards

    def map_text_to_shards(self, text: str) -> Dict[int, Set[str]]:
        """
        Map cleaned tokens to shard indices. Returns a dict: shard -> set(tokens).
        Useful for building inverted indices or seeding chaos pools.
        """
        tokens = self._clean_and_tokenize(text)
        shard_map: Dict[int, Set[str]] = {}
        for tok in tokens:
            shard = self._hash_token(tok)
            if shard not in shard_map:
                shard_map[shard] = set()
            shard_map[shard].add(tok)
        return shard_map

    def seed_chaos_pool(self, texts: Iterable[str]) -> None:
        """
        Populate self.shard_to_word with a representative token for each shard.
        If multiple tokens map to the same shard, the first seen token wins.
        """
        for text in texts:
            shard_map = self.map_text_to_shards(text)
            for shard, toks in shard_map.items():
                if shard not in self.shard_to_word:
                    # choose a deterministic representative (sorted)
                    rep = sorted(toks)[0]
                    self.shard_to_word[shard] = rep

    def get_shard_word(self, shard: int) -> str:
        """
        Return the representative word for a shard, or empty string if none.
        """
        return self.shard_to_word.get(shard, "")

    def text_to_shard_list(self, text: str) -> List[int]:
        """
        Convenience: return sorted list of shard indices for a text.
        """
        return sorted(self.map_text_to_shards(text).keys())
