
# coding: utf-8

# In[1]:

import json
from watson_developer_cloud import AlchemyLanguageV1
keyList=['cb738b85c0e2d0094894bcfe8c73d12d73543c35','af89b7da-4bab-4bec-aad6-85eaff5e2b90','b4632297-1c70-4de2-821b-95d2c3245d01','49662623-dd08-4f6e-871b-af1dec4cdaa1','a249944a-48e3-44cc-b481-248f7fa1e2d7']
keyUse=[True,False,False,False,False]
currentKey=0;
maxKey=5

alchemy_language = AlchemyLanguageV1(api_key=keyList[0])
from urllib.request import urlopen
import re


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
        found=False
        newKey=-1
        for i in range(currentKey,maxKey):
            if(keyUse[i] == False):
                found=True
                keyUse[i]=True
                newKey=i
                break

        if (not found) :
            print("Credentials, over used for the day, SORRY!")
            return None
        else:
            alchemy_language = AlchemyLanguageV1(api_key=keyList[newKey])
            sentence_sentiment(text_input)


# In[6]:

def listOfSentences (url,word):
    HTMl = urllib.request.urlopen(url).read()
    return re.findall(r"([^>=]*?word[^.<]*\.)",HTML)




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



def emotion_analysis(urlInput):
    return alchemy_language.emotion(url=urlInput)['docEmotions']


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
SIMILARITY = .5



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
            if(wordCount!=0):
                if sameWords >=wordCount*SIMILARITY:
                    similarSentences.append(potentialSentence)

        '''print (sameWords)
        print (wordCount)'''


    return similarSentences


def flipFlopped(sentenceArray):
    retArr=[]
    for sentence in sentenceArray:
        #print (sentence)
        if len(sentence.split()) >= MIN_WORDS :
            retSentenceArray = mostSimilarTo(sentence, sentenceArray)
        return retArr
        print ("The current sentence is: "+sentence+" and it is most similar to: ",end="")
        print (retSentenceArray)
        print (".")
            #if(  len(retSentenceArray) != 0):

             #   retSentenceArray.insert(0, sentence)
                #print(retSentenceArray)
             #   retStatus = compare_similar_sentences(retSentenceArray)
             #   retArr.append(sentence)
             #   retArr.append(retStatus)




'''
flipFlopped(['I hate war war is bad war is not good',
             'non no no yes hello hi there', 'These are not different and cool', 'these  are different and cool',
             'I love war war is okay war is fun',
             'War sounds good is good great war'])


flipFlopped(['The sky is blue today', 'the sky is green today'])



flipFlopped( ['Her late, great husband, Antonin Scalia, will forever be a symbol of American justice','As promised, I directed the Department of Defense to develop a plan to demolish and destroy ISIS -- a network of lawless savages that have slaughtered Muslims and Christians, and men, and women, and children of all faiths and all beliefs','Finally, I have kept my promise to appoint a justice to the United States Supreme Court, from my list of 20 judges, who will defend our Constitution'])

'''




import re

def fileio( filename ):
    text= None
    with open(filename) as file:
        text=file.read()

    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

    #print (sentences)
    retArray = flipFlopped(sentences)

    #print (retArray)
    for sentence in retArray:

        print ("Original sentence:", end=" ")
        print (sentence)
        print ("List of Flipflops: ",end="")
        print (sentence[0])
        print ("List of Consitent statements: ",end="")
        print (sentence[1])
        print ('\n')





def stdio( filename ):
    return

    # open the file
    # put it into a list of setneces

    # retArray = flipFlopped(sentenceArray)


    # print retArray

#fileio("test2.txt")


# In[32]:

import nltk
import gensim
