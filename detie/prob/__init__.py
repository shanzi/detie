#!/usr/bin/env python
# encoding: utf-8

from detie.prob.prob_emit import P as emit
from detie.prob.prob_start import P as start
from detie.prob.prob_trans import P as trans

MIN_FLOAT=0

_prob_trans_BE = trans['B'].get('E', MIN_FLOAT)
_prob_trans_MM = trans['M'].get('M', MIN_FLOAT)
_prob_trans = trans['B'].get('M', MIN_FLOAT) + trans['M'].get('E',MIN_FLOAT)
_prob_start = start.get('B')

def word_prob(text):
    len_ = len(text)
    if len_ <= 1: return MIN_FLOAT
    prob_b = emit['B'].get(text[0], MIN_FLOAT)
    prob_e = emit['E'].get(text[-1], MIN_FLOAT)
    if len_ == 2:
        return _prob_start + prob_b + prob_e + _prob_trans_BE
    else:
        prob_m = sum(emit.get(char, MIN_FLOAT) for char in text[1:-1])
        return _prob_start + _prob_trans + prob_m + _prob_trans_MM * (len_ - 3)


