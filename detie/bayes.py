from nltk.classify import PositiveNaiveBayesClassifier
from detie.data import PickleData, DictData


def features(words):
    return {char: True for char in words}

def train(spam_words, unlabeled_words):

    spams = list(map(features, spam_words))
    unlabeled = list(map(features, unlabeled_words))

    model = PositiveNaiveBayesClassifier.train(spams, unlabeled, 0.5)
    data = PickleData('bayesmodel.pickle')
    data.write(model)
    return model

def predictor():
    data = PickleData('bayesmodel.pickle')
    if data.exists:
        model = data.read()
    else:
        spam = DictData('spams.txt', encoding='utf8')
        unlabel = DictData('unlabeled.txt', encoding='utf8')
        model = train(spam.texts, unlabel.texts)

    def classify(word):
        pb = model.prob_classify(features(word))
        return pb.prob(1) > 0.95

    return classify
