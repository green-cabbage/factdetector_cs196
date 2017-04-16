
# coding: utf-8

# In[55]:

import json
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='cb738b85c0e2d0094894bcfe8c73d12d73543c35')

from urllib.request import urlopen
import re
from PyDictionary import PyDictionary


# In[27]:

def targeted_document_analysis(url_input, target_words):
    if (alchemy_language.targeted_sentiment(url=url_input, targets=target_words)["results"][0]['sentiment']['type'])=='neutral':
        return 0.0
    else:
        return (alchemy_language.targeted_sentiment(url=url_input, targets=target_words)["results"][0]['sentiment']['score'])
    pass


# In[28]:

def document_sentiment(url_input):
    if (alchemy_language.sentiment(url=url_input)['docSentiment']['score'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.sentiment(url=url_input)['docSentiment']['score'])


# In[29]:

def targeted_sentence_analysis(text_input, target_words):
    if (alchemy_language.targeted_sentiment(text=text_input, targets=target_words) ["results"][0]['sentiment']['type'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.targeted_sentiment(text=text_input, targets=target_words) ["results"][0]['sentiment']['score'])
    pass


# In[141]:

def sentence_sentiment(text_input):
    if (alchemy_language.sentiment(text=text_input)['docSentiment']['type'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.sentiment(text=text_input)['docSentiment']['score'])


# In[106]:

def listOfSentences (url,word):
    HTMl = urllib.request.urlopen(url).read()
    return re.findall(r"([^>=]*?word[^.<]*\.)",HTML)


# In[107]:

def compare_documents(array):
    prev = document_sentiment(array[0])
    for i in range (0,len(array)):
        temp = document_sentiment(array[i])
        if temp*prev<0:
            break
    if temp*prev<0:
        return False
    else:
        return True


# In[126]:

def compare_sentences(array):
    prev = float(sentence_sentiment(array[0]))
    for i in range (0,len(array)):
        temp = float(sentence_sentiment(array[i]))
        if temp+prev<0:
            break
    if temp*prev<0:
        return False
    else:
        return True


# In[115]:

def emotion_analysis(urlInput):
    return alchemy_language.emotion(url=urlInput)['docEmotions']


def compare_similar_sentences(subsequence):
    prev = float(sentence_sentiment(array[0]))
    for i in range (0,len(array)):
        temp = float(sentence_sentiment(array[i]))
        if temp+prev<0:
            break
    if temp*prev<0:
        return "Flip Flopped"
    else:
        return "Didn't Flop Flop"


#   Look through the stence array
#   put all the words in sentence into a dicitonary
#
#
#
def dumbWord(word):
    dumbWords= ["and", "or", "but", "nor", "so", "for", "yet", "after", "although", \
    "as", "as", "if", "as", "long", "as", "because", "before", "even", "if", "even", \
    "though", "once", "since", "so", "that", "though", "till", "unless", "until", "what", \
    "when", "whenever", "wherever", "whether", "while"]

    if (word.lower() in dumbWords):
        return True

    return False

THRESHOLD = 3
MIN_WORDS = 4
SIMILARITY = .6



def mostSimilarTo(sentence, sentenceArray):
    similarSentences = []
    sentenceDict = {}
    notDumbWords=0
    for word in sentence:
        word = word.lower()
        if not dumbWord(word):
            
            if word not in sentenceDict:
                sentenceDict.insert(word,1)
            else:    
                sentenceDict[word] += 1
                notDumbWords += 1
    

    for potentialSentence in sentenceArray:
        sameWords=0;
        if potentialSentence != sentence:
            for word in potentialSentence :
                word = word.lower()
                if word  in sentenceDict:
                    sameWords+=1


        if sameWords/notDumbWords >.6:
            similarSentences.append(potentialSentence)

    return similarSentences


def flipFlopped(sentenceArray):
    for sentence in sentenceArray:
        if len(sentence) >= MIN_WORDS :
            retSentenceArray = mostSimilarTo(sentence, sentenceArray)
            compare_similar_sentences(retSentenceArray)



# In[142]:

emotion_analysis('charliechaplin.com/en/synopsis/articles/29-The-Great-Dictator-s-Speech')


# In[143]:

targeted_document_analysis("http://docs.oracle.com/cd/E64107_01/bigData.Doc/data_processing_bdd/src/rdp_de_sentiment_svm.html","sentiment")


# In[32]:

document_sentiment("http://docs.oracle.com/cd/E64107_01/bigData.Doc/data_processing_bdd/src/rdp_de_sentiment_svm.html")


# In[33]:

targeted_sentence_analysis("The quick brown fox jumped over the lazy dog","dog")


# In[144]:

sentence_sentiment('That was okay!')


# In[121]:

listOfSentences ('http://math.hws.edu/javanotes/c8/s2.html','computer')


# In[ ]:




# In[145]:

compare_sentences(['That was great!','That was okay!'])


# In[ ]:



