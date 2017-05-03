import json
from watson_developer_cloud import AlchemyLanguageV1
keyList=['cb738b85c0e2d0094894bcfe8c73d12d73543c35','af89b7da-4bab-4bec-aad6-85eaff5e2b90','b4632297-1c70-4de2-821b-95d2c3245d01','49662623-dd08-4f6e-871b-af1dec4cdaa1','a249944a-48e3-44cc-b481-248f7fa1e2d7']
keyUse=[True,False,False,False,False]
currentKey=0;
maxKey=5
alchemy_language = AlchemyLanguageV1(api_key=keyList[0])
from urllib.request import urlopen
import re
from gensim.models import word2vec
from gensim import models
from gensim.models.keyedvectors import KeyedVectors
pathToBinVectors='./GoogleNews-vectors-negative300.bin'
print ("Loading the data file... Please wait...")
model1=KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)
print ("Successfully loaded 3.6 G bin file!")
import numpy as np
import math
import scipy
from random import sample
import sys
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
SIMILARITY=.8
meme=SentimentIntensityAnalyzer()
num_features=300
index2word_set=set(model1.index2word)

# In[2]:

def targeted_document_analysis(url_input, target_words):
    if (alchemy_language.targeted_sentiment(url=url_input, targets=target_words)["results"][0]['sentiment']['type'])=='neutral':
        return 0.0
    else:
        return (alchemy_language.targeted_sentiment(url=url_input, targets=target_words)["results"][0]['sentiment']['score'])
    pass


# In[3]:

def document_sentiment(url_input):
    if (alchemy_language.sentiment(url=url_input)['docSentiment']['score'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.sentiment(url=url_input)['docSentiment']['score'])


# In[4]:

def targeted_sentence_analysis(text_input, target_words):
    if (alchemy_language.targeted_sentiment(text=text_input, targets=target_words) ["results"][0]['sentiment']['type'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.targeted_sentiment(text=text_input, targets=target_words) ["results"][0]['sentiment']['score'])
    pass


# In[5]:

def sentence_sentiment(text_input):
    try:
        if (alchemy_language.sentiment(text=text_input)['docSentiment']['type'])=='neutral':
            return 0.0
        else:
            return(alchemy_language.sentiment(text=text_input)['docSentiment']['score'])
    except:
        return None

# In[6]:

def listOfSentences (url,word):
    HTMl = urllib.request.urlopen(url).read()
    return re.findall(r"([^>=]*?word[^.<]*\.)",HTML)




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
            #print("Didn't Flop Flop")re
            retArray[1].append(subsequence[i])

    return retArray


def avg_feature_vector(words, model, num_features):
    featureVec = np.zeros((num_features,), dtype="float32")



    nwords=0
    for word in words:
        if word in index2word_set:
            featureVec = np.add(featureVec, model[word])
            nwords = nwords+1
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

