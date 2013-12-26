from snownlp import SnowNLP
from marisa_trie import Trie

def sentiment(keywords_trie, text):
    words = set()
    for i in range(len(text)):
        prefixes = keywords_trie.prefixes(text[i:])
        if prefixes:
            words.union(prefixes)
    if len(words):
        return (words, nlp.sentiments - 0.5)
    else: return None, 0
