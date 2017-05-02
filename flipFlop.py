from urllib.request import urlopen
import re
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
pathToBinVectors='/Users/Anmol/Desktop/CS196/factdetector_cs196/GoogleNews-vectors-negative300.bin'
print ("Loading the data file... Please wait...")
model1 =  KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True) 
print ("Successfully loaded 3.6 G bin file!")
import numpy as np
import math
import scipy
from random import sample
import sys
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
SIMILARITY=.7


def sentence_sentiment(sentence):
    ss=SentimentIntensityAnalyzer().polarity_scores(sentence)
    return ss['compound']


def compare_similar_sentences(subsequence ):
    retArray=[]
    retArray.append([])
    retArray.append([])
    #print (retArray)
    prev = float(sentence_sentiment(subsequence[0]))
    for i in range (1,len(subsequence)):
        temp = float(sentence_sentiment(subsequence[i]))
        if temp*prev <= 0:
            #print("Flip Flopped")
            retArray[0].append(subsequence[i])
        else:
            #print("Didn't Flop Flop")
            retArray[1].append(subsequence[i])

    return retArray


def avg_feature_vector(words, model, num_features):
    featureVec = np.zeros((num_features,), dtype="float32")
    index2word_set=set(model.index2word)
    nwords=0
    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])
    if(nwords>0):
        featureVec = np.divide(featureVec, nwords)
    return featureVec


def mostSimilarTo(sentence, sentenceArray):
    similarSentences = []
    sentenceDict = {}
    notDumbWords=0
    sentence_1_avg_vector = avg_feature_vector(sentence.split(), model1, num_features=300)

    for potentialSentence in sentenceArray:
        if potentialSentence != sentence:
            sentence_2_avg_vector = avg_feature_vector(potentialSentence.split(), model1, num_features=300)
            sen1_sen2_similarity =  1 - scipy.spatial.distance.cosine(sentence_1_avg_vector,sentence_2_avg_vector)
            if sen1_sen2_similarity>SIMILARITY:
                similarSentences.append(potentialSentence)

    return similarSentences


def flipFlopped(sentenceArray):
    retArr=[]
    for sentence in sentenceArray:
        retSentenceArray = mostSimilarTo(sentence, sentenceArray)
        if(  len(retSentenceArray) != 0):
            retSentenceArray.insert(0,sentence)
            retStatus = compare_similar_sentences(retSentenceArray)
            retStatus.insert(0, sentence) 
            retArr.append(retStatus)
    return retArr



# [
# [ sentence, flipFlopLIST[], ConsistentLIST[] ]
# ,[sentence, flipFlopLIST, ConsistentLIST]
# ]

print ( flipFlopped(['The sky is blue today', 'the sky is green today']) )
print(flipFlopped(['I hate war war is bad war is not good',
             'non no no yes hello hi there', 'These are not different and cool', 'these  are different and cool',
             'I love war war is okay war is fun',
             'War sounds good is good great war']))
# flipFlopped( ['Her late, great husband, Antonin Scalia, will forever be a symbol of American justice','As promised, I directed the Department of Defense to develop a plan to demolish and destroy ISIS -- a network of lawless savages that have slaughtered Muslims and Christians, and men, and women, and children of all faiths and all beliefs','Finally, I have kept my promise to appoint a justice to the United States Supreme Court, from my list of 20 judges, who will defend our Constitution'])


'''
flipFlopped(['I hate war war is bad war is not good',
             'non no no yes hello hi there', 'These are not different and cool', 'these  are different and cool',
             'I love war war is okay war is fun',
             'War sounds good is good great war'])
# 
'''