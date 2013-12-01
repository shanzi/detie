from detie.utils import logger
from detie.data import DictData
from marisa_trie import Trie

def run():
    logger.info("Building trie tree")
    dict_data = DictData('COAE_Known_dict.txt')
    trie = Trie(dict_data)
    logger.info("Trie tree build success")
