#!/usr/bin/env python
# encoding: utf-8

import re

RE_MENTION = re.compile(ur"@\S+")
RE_CN = re.compile(ur"[^\u4E00-\u9FA5]+")

def divide(text):
    text = RE_MENTION.sub(u'', text)
    return RE_CN.split(text)

def get_new_string(trie, text):
    if len(text) == 1:return None
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
            newstr += text[i]
    if newstr and len(newstr)>1:
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
