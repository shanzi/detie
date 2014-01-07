from nltk.classify import NaiveBayesClassifier
from detie.data import PairData, PickleData


def features(words):
    return {char: True for char in words}

def train_sentiments_classifier():
    pairs = PairData('sentiments.txt', 'utf8')
    model = NaiveBayesClassifier.train(pairs)
    data = PickleData('sentiments.pickle')
    data.write(model)
    return model

def estimate_neu(tags):
    sum_ = 0
    for w, t in tags:
        if t.endswith('n'): sum_+=1

    if tags[-1][-1].endswith('n'):
        return float(sum_)/len(tags) * 1.5
    else:
        return float(sum_)/len(tags)

def sentiment_classifier():
    data = PickleData('sentiments.pickle')
    if data.exists:
        model = data.read()
    else:
        model = train_sentiments_classifier()
    from snownlp import SnowNLP
    def classify(word):
        nlp = SnowNLP(word)
        neu = 1 if (estimate_neu(nlp.tags)>0.6) else 0
        senti = nlp.sentiments - 0.5
        prob = model.prob_classify(features(word))
        prob_senti = prob.prob(1) -  prob.prob(-1) 
        if neu: return 0
        else:
            fs = (prob_senti + senti)/3
            if fs >= 0.25: return 1 
            elif fs <= -0.25: return -1
            else: return 0

    return classify




