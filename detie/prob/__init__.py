#!/usr/bin/env python
# encoding: utf-8

from detie.prob.prob_emit import P as emit
from detie.prob.prob_start import P as start
from detie.prob.prob_trans import P as trans

MIN_FLOAT=0

def word_prob(text):
    len_ = len(text)
    if len_ <= 1: return emit['S'].get(text, MIN_FLOAT)
    prob_b = emit['B'].get(text[0], MIN_FLOAT)
    prob_e = emit['E'].get(text[-1], MIN_FLOAT)
    return (-max(prob_b, prob_e), -min(prob_b, prob_e), prob_e*prob_b, abs(prob_b-prob_e))
