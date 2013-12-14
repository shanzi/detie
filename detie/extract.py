#!/usr/bin/env python
# encoding: utf-8

import re

from detie.data import SetData 

RE_MENTION = re.compile(ur"@\S+")
RE_NON_CN = re.compile(ur"[^\u4E00-\u9FA5]+")
RE_NUM = re.compile(
ur"[\u591a\u4e24\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07\u4ebf\u51e0]+")

IGNORE_SINGLE_CHARS = SetData('ignore_single_chars.txt')
RE_SINGLE_CHAR = re.compile(IGNORE_SINGLE_CHARS.to_regexp())


def divide(text):
    text = RE_MENTION.sub(u' ', text)
    text = RE_SINGLE_CHAR.sub(u' ', text)
    return RE_NON_CN.split(text)

def fullcut(text):
    list_ = []
    len_ = len(text)
    if not text or len_<2: return list_
    if len_<=5:
        list_.append(text)
    else:
        for j in [2, 3, 4]:
            for i in range(len_-j+1):
                list_.append(text[i:i+j])
    return list_

def get_new_string(trie, text):
    if len(text) <= 1:return None
    new_string_list = []
    newstr = ''
    for i in range(len(text)):
        subtext = text[i:]
        prefixes = trie.prefixes(subtext)
        if prefixes:
            for prefix in prefixes:
                list_ = get_new_string(trie, subtext[len(prefix):])
                if list_: new_string_list+=list_
                if len(newstr)==2 and len(prefix)==2:
                    new_string_list.append(newstr+prefix)
            break
        else:
            newstr += subtext[0]
    return fullcut(newstr) + new_string_list

def extract_new_string(trie, text):
    texts = divide(text)
    list_ = []
    for text in texts:
        if len(text)>40: print '!',
        elif len(text)>20: print '.',
        new_str_list = get_new_string(trie, text)
        if new_str_list: list_+=new_str_list
    return list_
