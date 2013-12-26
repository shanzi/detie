from collections import Counter

from marisa_trie import Trie

from detie.utils import logger
from detie.data import DictData, NLPIRXMLData, IdData
from detie.extract import extract_new_string
from detie.prob import word_prob
from detie.bayes import predictor, retrain as retrain_bayes
from detie.sentiments import sentiment

import multiprocessing
import re

DOCID_RE = re.compile(ur'^<doc\d+>')

_global = {}

COUNT_STEP = 2000

def build_trie():
    logger.info("Building trie tree")
    dict_data = DictData('COAE_Known_dict.txt')
    trie = Trie(dict_data)
    logger.info("Trie tree build success")
    return trie

def build_sentiments_trie():
    set_data = DictData('output.txt')
    trie = Trie(set_data)
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


def sentiments_process(texts):
    trie = _global['s_trie']
    list_ = []
    doc = u''
    for text in texts:
        w, s = sentiment(trie, text)
        if w:
            match = DOCID_RE.search(text)
            if match: doc = unicode(match.group())
            if not doc: continue
            list_.append((doc, w, s))
    return list_

def sentiments():
    sentiment_trie = build_sentiments_trie()
    _global['s_trie'] = sentiment_trie
    counter_positive = Counter()
    counter_negtive = Counter()
    counter_neutral = Counter()
    doc = {}
    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpu_count)
    corpus = load_corpus()
    sentiment_pair_groups = pool.map(sentiments_process, corpus.texts, COUNT_STEP)
    for sentiment_pairs in sentiment_pair_groups:
        for doc, words, sentiment_value in sentiment_pairs:
            print doc, words, sentiment_value
            if not doc: continue
            if sentiment_value > 0.25:
                for w in words: counter_positive[w]+=1
            elif sentiment_value < -0.25:
                for w in words: counter_negtive[w]+=1
            else:
                for w in words: counter_neutral[w]+=1

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
