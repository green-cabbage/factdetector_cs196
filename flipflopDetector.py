
# coding: utf-8

# In[3]:

import json
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='cb738b85c0e2d0094894bcfe8c73d12d73543c35')

from urllib.request import urlopen
import re


# In[4]:

def targeted_document_analysis(url_input, target_words):
    if (alchemy_language.targeted_sentiment(url=url_input, targets=target_words)["results"][0]['sentiment']['type'])=='neutral':
        return 0.0
    else:
        return (alchemy_language.targeted_sentiment(url=url_input, targets=target_words)["results"][0]['sentiment']['score'])
    pass


# In[5]:

def document_sentiment(url_input):
    if (alchemy_language.sentiment(url=url_input)['docSentiment']['score'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.sentiment(url=url_input)['docSentiment']['score'])


# In[6]:

def targeted_sentence_analysis(text_input, target_words):
    if (alchemy_language.targeted_sentiment(text=text_input, targets=target_words) ["results"][0]['sentiment']['type'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.targeted_sentiment(text=text_input, targets=target_words) ["results"][0]['sentiment']['score'])
    pass


# In[7]:

def sentence_sentiment(text_input):
    if (alchemy_language.sentiment(text=text_input)['docSentiment']['type'])=='neutral':
        return 0.0
    else:
        return(alchemy_language.sentiment(text=text_input)['docSentiment']['score'])


# In[8]:

def listOfSentences (url,word):
    HTMl = urllib.request.urlopen(url).read()
    return re.findall(r"([^>=]*?word[^.<]*\.)",HTML)


# In[9]:

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


# In[118]:

def compare_sentences(array):
    prev = float(sentence_sentiment(array[0]))
    for i in range (0,len(array)):
        temp = float(sentence_sentiment(array[i]))
        if temp+prev<0:
            break
    if temp+prev<0:
        return False
    else:
        return True


# In[119]:

def emotion_analysis(urlInput):
    return alchemy_language.emotion(url=urlInput)['docEmotions']


# In[166]:

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
#   Look through the stence array
#   put all the words in sentence into a dicitonary
#
#
#
def dumbWord(word):
    dumbWords= ["and", "or", "but", "nor", "so", "for", "yet", "after", "although",     "as", "as", "if", "as", "long", "as", "because", "before", "even", "if", "even",     "though", "once", "since", "so", "that", "though", "till", "unless", "until", "what",     "when", "whenever", "wherever", "whether", "while"]

    if (word.lower() in dumbWords):
        return True

    return False

THRESHOLD = 3
MIN_WORDS = 3
SIMILARITY = .6



def mostSimilarTo(sentence, sentenceArray):
    similarSentences = []
    sentenceDict = {}
    notDumbWords=0
    for word in sentence.split():
        #print (word)
        word = word.lower()
        if not dumbWord(word):
            notDumbWords += 1
            if word not in sentenceDict:
                sentenceDict[word]=1
            else:    
                sentenceDict[word] += 1
               
    

    for potentialSentence in sentenceArray:
        sameWords=0
        wordCount =0
        if potentialSentence != sentence:
            
            for word in potentialSentence.split() :
                word = word.lower()
                if not dumbWord(word):
                    wordCount+=1
                    if word  in sentenceDict:
                        sameWords+=1

       # print (sameWords)
        #print (wordCount)
        if(wordCount!=0):
            if sameWords >=MIN_WORDS:
                similarSentences.append(potentialSentence)

    return similarSentences


def flipFlopped(sentenceArray):
    retArr=[]
    for sentence in sentenceArray:
        if len(sentence.split()) >= MIN_WORDS :
            
            retSentenceArray = mostSimilarTo(sentence, sentenceArray)
            
            if(  len(retSentenceArray) != 0):
               
                retSentenceArray.insert(0, sentence)
                #print(retSentenceArray)
                retStatus = compare_similar_sentences(retSentenceArray)
                print ("Original sentence:", end=" ")
                print (sentence)
                print ("List of Flipflops: ",end="") 
                print (retStatus[0])
                print ("List of Consitent flops: ",end="") 
                print (retStatus[1])
                print ('\n')
                retArr.append(retStatus)
            
    return retArr


# In[170]:

flipFlopped(['I hate war war is bad war is not good','I love war war is okay war is fun', 'War sounds good is good great war'])


# In[ ]:




# In[ ]:



