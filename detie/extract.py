#!/usr/bin/env python
# encoding: utf-8

import re

from detie.data import SetData 

RE_MENTION = re.compile(ur"@\S+")
RE_NON_CN = re.compile(ur"[^\u4E00-\u9FA5]+")
RE_NUM = re.compile(
ur"[\u591a\u4e24\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07\u4ebf\u51e0]+")

IGNORE_SINGLE_CHARS = SetData('ignore_single_chars.txt')

def divide(text):
    text = RE_MENTION.sub(u' ', text)
    return RE_NON_CN.split(text)

def preaccept(text):
    if len(text)>5:
        return False
    elif len(text)>1: 
        if RE_NUM.match(text[:-1]):
            return False
        return True
    return False

def get_new_string(trie, text):
    if len(text) <= 1:return None
    new_string_list = []
    newstr = ''
    for i in range(len(text)):
        subtext = text[i:]
        prefixes = trie.prefixes(subtext)
        if prefixes:
            for prefix in prefixes:
                if len(prefix)<len(subtext):
                    list_ = get_new_string(trie, subtext[len(prefix):])
                    if list_: new_string_list+=list_
            break
        else:
            char = subtext[0]
            if char in IGNORE_SINGLE_CHARS:
                list_ = get_new_string(trie, subtext[1:])
                if list_: new_string_list+=list_
                break
            else:
                newstr += subtext[0]
    if newstr and preaccept(newstr):
        return [newstr,] + new_string_list
    else:
        return new_string_list

def extract_new_string(trie, text):
    texts = divide(text)
    list_ = []
    for text in texts:
        new_str_list = get_new_string(trie, text)
        if new_str_list: list_+=new_str_list
    return list_
