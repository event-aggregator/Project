#!/usr/bin/env python
# coding: utf-8

# In[22]:


import re
import nltk
from nltk import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Preprocessing and tokenizing
def preprocessing(line):
    for i in range(len(line)):
        line[i]= line[i].lower()
        line[i] = re.sub('[%s]' % re.escape(",."), ' ', line[i]) # удалит символы пунктуации
        line[i] = stemmer.stem(line[i])
    return line

stemmer = SnowballStemmer("english") 

a=['C++', 'Python', 'Java', 'C', 'HTML', 'CSS', 'JavaScript', 'C#', 'Go', 'Ruby','Perl', 'Pascal', 'PHP', 'Haskell', 'Swift', 'F#', 'Erlang', 'Kotlin','Scala', 'Delphi', 'Basic', 'LISP', 'D', 'Clojure', 'R', 'MATLAB', 'Objective-C','Elm', 'Elixir', 'Dart', 'TypeScript', 'Lua', 'Prolog']
b = ['Backend development','Frontend development','UI UX design','Machine learning','AI (Artificial Intelligence)','Data sience','Mobile app development','Game development','DevOps','Big Data','Software engineering','Information security','Deep Learning','Meet Up','Discuss Speak club','Learn forum','Web technology','cloud technology']

#блок параметров, которые передаются от backend из другой программы
num = #чисто тем

c = #интересы пользователя из анкеты в формате list (например: c = ['CSS', 'Erlang', 'Machine learning', 'DevOps', 'Game development'])

key = #ключевые слова для каждой темы в формате list (key[i] - список ключевый слов i темы, key[i][j] - j ключевое слово в i теме)
#конец блока


#кластеризация интересов и тем   
key_pr = []
c_pr = []
key_pr = key.copy()
key_pr = preprocessing(key)
c_pr = preprocessing(c)
c_str = ' '.join(c_pr)
lines_for_predicting =[]
lines_for_predicting= key_pr.copy()
lines_for_predicting.append(c_str)

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(key_pr)

kmeans = KMeans(n_clusters=num).fit(tfidf)

v = kmeans.predict(tfidf_vectorizer.transform(lines_for_predicting))
#print(v)

i = 0
top = 10
while top == 10:
    if v[i]==v[num]:
        top = i
    else:
        i+=1
#важно! данные для анализа
#top - номер подходящей темы

