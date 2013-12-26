from snownlp import SnowNLP
from nltk.classify import NaiveBayesClassifier
from detie.data import PairData


def features(words):
    return {char: True for char in words}

def train_sentiments_classifier():
    pairs = PairData('sentiment.txt')
    model = NaiveBayesClassifier.train(pairs)
    data = PickleData('sentiments.pickle')
    data.write(model)
    return model

def sentiment_classifier():
    data = PickleData('bayesmodel.pickle')
    if data.exists:
        model = data.read()
    else:
        model = train_sentiments_classifier()

    def classify(word):
        nlp = SnowNLP(word)
        senti = nlp.sentiments - 0.5
        prob = model.prob_classify(features(word))
        prob_senti = prob.prob(-1) * - 0.5 + prob.prob(1) * 0.5
        return senti + prob_senti

    return classify




