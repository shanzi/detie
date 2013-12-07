from collections import Counter

from marisa_trie import Trie

from detie.utils import logger
from detie.data import DictData, NLPIRXMLData 
from detie.extract import extract_new_string
from detie.prob import word_prob


def build_trie():
    logger.info("Building trie tree")
    dict_data = DictData('COAE_Known_dict.txt')
    trie = Trie(dict_data)
    logger.info("Trie tree build success")
    return trie

def load_corpus():
    logger.info("Loading corpus data")
    corpus_data = NLPIRXMLData("NLPIR_weibo_content_corpus.xml") 
    logger.info("Corpus data loaded")
    return corpus_data

def count_new_strings():
    trie = build_trie()
    corpus = load_corpus()
    counter = Counter()
    i=0
    sum_ = float(23E4)
    for text in corpus.texts:
        if not text: continue
        new_strings = extract_new_string(trie, text)
        for str_ in new_strings:
            counter[str_] += 1
        i+=1
        if i%1000==0:
            logger.info("Computing: %.2f%% - [%d]" % (i/sum_*100, len(counter)))
    logger.info("Computing finished")
    return counter

def score():
    data = DictData('rank.txt', 'utf8')
    for text in data.texts:
        a,b,c,d = word_prob(text)
        if (a>=4.5 and c>=33):
            l = u"%-20s %3.5f %3.5f %3.5f %3.5f" % (text,a,b,c,d)
            print l.encode('utf8')
        else:
            l = u"%20s %3.5f %3.5f %3.5f %3.5f" % (text,a,b,c,d)
            print l.encode('utf8')


def run():
    counter = count_new_strings()
    for word, count in counter.most_common(1000):
        wp = word_prob(word)
        l = u"%s [%f] (%d)" % (word, wp, count)
        print l.encode('utf8')
