#!/usr/bin/env python
# coding: utf-8

import re
import nltk
from nltk import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans



# Preprocessing and tokenizing
def preprocessing(line):
    for i in range(len(line)):
        line[i] = line[i].lower()
        line[i] = re.sub('[%s]' % re.escape(",.()"), ' ', line[i])  # удалит символы пунктуации
        line[i] = stemmer.stem(line[i])
    return line


stemmer = SnowballStemmer("english")

# блок параметров, которые передаются от backend из другой программы
# num - чисто тем

# user - интересы пользователя из анкеты в формате list (например: user = ['CSS', 'Erlang', 'Machine learning', 'DevOps', 'Game development'])

# key - ключевые слова для каждой темы в формате list (key[i] - список ключевый слов i темы, key[i][j] - j ключевое слово в i теме)
# конец блока

user = ['CSS', 'Erlang', 'Machine learning', 'DevOps', 'Game development']

def clast(user):
    # кластеризация интересов и тем
    key = ["tsubhead, game, club, bar, intern, kjhkjh, learn, meet, mast, play",
            "apach, hadoop, nifi, hdfs, python, yarn, manag, mapr, node, educ",
            "appl, microsoft, googl, numb, iwork, keynot, excel, data, powerpoint, outlook",
            "web, uniti, appl, excel, css, javascript, html, bord, frontend, skill",
            "process, kafka, work, surfaceview, wordart, tech, expos, icollect, market, activ",
            "kafka, googl, stream, apach, appl, topic, microsoft, zookeep, keynot, iwork",
            "meet, speak, lcampus, intern, nativ, talk, chat, discuss, club, speed",
            "java, develop, digit, juni, custom, web, gamedev, learn, bord, work",
            "bord, web, html, appl, backend, seni, collaps, css, googl, netbean"]
    num = len(key)
    key_pr = []
    user_pr = []
    key_pr = key.copy()
    key_pr = preprocessing(key)
    user_pr = preprocessing(user)
    user_str = ' '.join(user_pr)
    lines_for_predicting = []
    lines_for_predicting = key_pr.copy()
    lines_for_predicting.append(user_str)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(key_pr)

    kmeans = KMeans(n_clusters=num).fit(tfidf)

    v = kmeans.predict(tfidf_vectorizer.transform(lines_for_predicting))

    i = 0
    top = 10
    while top == 10:
        if v[i] == v[num]:
            top = i
        else:
            i += 1
    return v[i]

