from snownlp import SnowNLP
from marisa_trie import Trie

def sentiment(keywords_trie, text, skip):
    words = set()
    for i in range(len(text)):
        prefixes = keywords_trie.prefixes(text[i:])
        for prefix in prefixes:
            words.add(prefix)
    if len(words):
        if skip%10 == 0:
            nlp = SnowNLP(text)
            return (words, nlp.sentiments - 0.5)
        else:
            return (words, -2)
    else: return None, 0

def sentiment_gather(word, pos, neutral, neg):
    nlp = SnowNLP(word)
    senti = nlp.sentiments - 0.5
    all_count = pos + neutral + neg
    senti_count = all_count if all_count > 100 else 50
    rs =  (senti_count * senti + 0.5 * pos + neg * -0.5)/(all_count + senti_count)
    if rs > 0.3:return 1
    if rs < -0.3:return -1
    else: return 0

