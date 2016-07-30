#-*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk
import lda
import lda.datasets
import json
import re

#重写build_analyzer方法，加入词干处理
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        english_stemmer = nltk.stem.SnowballStemmer('english')
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

#提取文档向量
def getdoc(url):
    fs = open(url)
    all_doc = []
    pkg = []
    for line in fs.readlines():
        js = json.loads(line)
        text=getText(js['description'])
        pkg.append(js['localid'])
        all_doc.append(text)
    return all_doc,pkg

#去除文档中的非关键字字符
def getText(text):
    s2=re.compile('[^A-Za-z0-9]')
    #text=re.sub(s1,'. ',text)
    text=re.sub(s2,' ',text)
    return text

#提取文本特征向量
def doc2vec(doclist):
    documents=np.array(doclist)
    #stop_words停止词，binary频数布尔化，min_df词频最低限制
    vector=StemmedCountVectorizer(stop_words='english',binary=False, decode_error='ignore',min_df=1)
    #文档-词频向量（可支持出现或者不出现）
    vec=vector.fit_transform(documents).todense()
    print(vector.fit_transform(documents).todense())
    #词序号
    print vector.vocabulary_
    voc=sorted(vector.vocabulary_.iteritems(),key=lambda a:a[1],reverse=False)
    vocab=[]
    for word in voc:
        vocab.append(word[0])
    vocab=np.array(vocab)
    return vec,vocab

#使用lda提取主题以及主题词
def mylda(X,titles,vocab):
    X=np.array(X)
    model = lda.LDA(n_topics=10, n_iter=1500, random_state=1)
    model.fit(X)
    topic_word = model.topic_word_
    n_top_words = 10
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    doc_topic = model.doc_topic_
    for i in range(30):
        print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    return 0

url='test.txt'
all_doc,pkg=getdoc(url)
X,vocab=doc2vec(all_doc)
mylda(X,pkg,vocab)
