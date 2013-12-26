from collections import Counter

from marisa_trie import Trie

from detie.utils import logger
from detie.data import DictData, NLPIRXMLData
from detie.extract import extract_new_string
from detie.prob import word_prob
from detie.bayes import predictor, retrain as retrain_bayes
from detie.sentiments import sentiment_classifier

import multiprocessing
import re

DOCID_RE = re.compile(ur'^<doc\d+>', re.IGNORECASE)

_global = {}

COUNT_STEP = 2000

def build_trie():
    logger.info("Building trie tree")
    dict_data = DictData('COAE_Known_dict.txt')
    trie = Trie(dict_data)
    logger.info("Trie tree build success")
    return trie


def load_corpus():
    logger.info("Loading corpus data")
    #corpus_data = NLPIRXMLData("NLPIR_weibo_content_corpus.xml", encoding='gbk') 
    corpus_data = DictData('COAE2014_task3', encoding='gbk')
    logger.info("Corpus data loaded")
    return corpus_data

def extract_process(texts):
    list_ = []
    trie = _global['trie']
    for text in texts:
        if not text: continue
        list_ += extract_new_string(trie, text)
    return list_

def count_new_strings():
    _global['trie'] = build_trie()
    corpus = load_corpus()
    counter = Counter()
    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpu_count)
    logger.info('Create pool of %d processes' % cpu_count)
    i=0
    sum_ = float(9999000)/COUNT_STEP
    groups = corpus.block_groups(cpu_count, COUNT_STEP)
    for group in groups:
        new_string_groups = pool.map(extract_process, group)
        for new_strings in new_string_groups:
            for str_ in new_strings:
                counter[str_] += 1
        i+=cpu_count
        logger.info("Computing: %.2f%% - [%d]" % (i/sum_*100, len(counter)))
    logger.info("Computing finished")
    return counter

def sentiments():
    data = DictData('output.txt')
    classify = sentiment_classifier()
    for word in data:
        c = classify(word)
        l =  u"2.3 %s %s" % (word, c)
        print l.encode('utf8')

def run():
    counter = count_new_strings()
    p = predictor()
    limit = 12000
    for word, count in counter.most_common():
        if not p(word):
            l = word
            print l.encode('utf8')
            limit -= 1
            if limit <= 0: return
