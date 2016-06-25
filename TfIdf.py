# -*- coding: utf-8 -*
import nltk
import re
import math
import json

def getTxt(url):
    fs=open(url)
    all_text=[]
    pkg=[]
    for line in fs.readlines():
        js=json.loads(line)
        pkg.append(js['localid'])
        all_text.append(js['description'])
    return all_text

def getText(text):
    #s1=re.compile('\.')
    s2=re.compile('[^A-Za-z0-9-]')
    #text=re.sub(s1,'. ',text)
    text=re.sub(s2,' ',text)
    return text

def getWordlist(all_text):
    wordlist=[]
    s = nltk.stem.SnowballStemmer('english')
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for text in all_text:
        text=getText(text)
        words=nltk.word_tokenize(text)
        for word in words:
            if word not in wordlist:
                wordlist.append(s.stem(word))
    return wordlist

def getTf(text):
    text=getText(text)
    words=nltk.word_tokenize(text)
    wordlist=[]
    lemmatizer = nltk.stem.WordNetLemmatizer()
    s = nltk.stem.SnowballStemmer('english')
    for word in words:
        wordlist.append(s.stem(word))
    wordnum=float(len(wordlist))
    TF={}
    for word in wordlist:
        if word not in TF.iterkeys():
            TF[word]=wordlist.count(word)/wordnum
    return TF

def getIdf(all_text):
    wordlist=getWordlist(all_text)
    IDF={}
    docnum=float(len(all_text))
    for word in wordlist:
        if nltk.pos_tag([word])[0][1] in ('NN','IN','JJR','JJ','RB','CD'):
            isnum=0
            for text in all_text:
                text=getText(text)
                textwordlist=getWordlist([text])
                if  word in textwordlist:
                    isnum=+isnum+1
            IDF[word]=math.log(docnum/(isnum+1))
        else:
            IDF[word]=0.0
    return IDF

def main(all_text):
    IDF=getIdf(all_text)
    for text in all_text:
        TF=getTf(text)
        RE={}
        for word in TF.iterkeys():
            RE[word]=TF[word]*IDF[word]
        RE=sorted(RE.iteritems(),key=lambda Re:Re[1],reverse=True)
        print all_text.index(text)+1,RE[0:4]
    return 0
