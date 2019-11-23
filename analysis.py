#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re
import math
import nltk
import pymorphy2
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
from nltk import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
# Plots
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
                                                     
df = get_dataframe()
#nltk.download('punkt')

def clean_tweet(tweet):
    if pd.isna(tweet)==False :
        tweet = re.sub('http\S+\s*', '', tweet) 
        tweet = re.sub('href\S+\s*', '', tweet)
        tweet = re.sub('www\s*', '', tweet)
        tweet = re.sub('\s\w\s', ' ', tweet)
        tweet = re.sub("\d+|-\d+", ' ',tweet)
        tweet = re.sub('<\w*\s\w+\W+\s*\w+\W+\w*\W*\w*\W+>', ' ', tweet)
        tweet = re.sub('</*\w*/*>*', ' ', tweet)
        tweet = re.sub('&\w+', ' ', tweet)
        tweet = re.sub('\W{2}', ' ', tweet)
        tweet = re.sub('\n', ' ', tweet)
        tweet = re.sub('\t', ' ', tweet) 
        tweet = re.sub('\xa0', ' ', tweet)
        tweet = re.sub('-грабл', ' ', tweet)
        tweet = re.sub('\[\w+\]',' ', tweet) 
        tweet = re.sub('•|//|\*|=+|↔|--|——| –| —| -| -',' ',tweet)
        tweet = re.sub('@\S+', '', tweet)
        tweet = re.sub('style|text|align| scr |justify| с | pm |gdg| sb |rte|width|font|—| gc |size|bgcolor|dcdcdc|rsvp|height| alt | px | src |colspan| st | spb |class| gt | lt | br | p |center|left', ' ', tweet)
        tweet = re.sub('[%s]' % re.escape("!''""#$%&()“”«»*╰+,№./:;<=>✔✓®™?@[\]^_`{|}~📍🥳🚨🎢🏰👍🤙👌🚠🙆🤩🎤😶🤠🏨🀄🌾🚂🧗🏕🤡🌟🏃♻️😱🧠🚶 😋👇✨🕺💃🥂🏬🚩📆⏰🙂😉☕🧗📢💬😎❗✊🍿📌🤗🎁🌎🔥🦸‍♂️🦸‍♀️👩‍🚀✅👨‍🎨👨‍✈️👩‍✈️⚡🔋📱🕵🏻‍♂️📨🧳🤝👋🏼🎡😃💟🥏☝️🧾❤️💰🚀💡🤔👉🥒🌞🙍‍♂😊😌🗣☮💥🏠📝📞"), ' ', tweet) # удалит символы пунктуации
    return tweet 
    
df1 = df.copy()
#df1 = pd.read_excel('Data (1).xlsx')
# dropping passed columns 
df1.drop(["id", "address","date","time","link","image","city"], axis = 1, inplace = True) 

df2 = df.copy()
df2.drop(["id", "address","date","time","link","image","city"], axis = 1, inplace = True) 

for i in range(df1.shape[0]):
    if pd.isna(df1['description'][i])==True :
        df1['description'][i] = 'No description'
df1['Combined'] = df1.fillna(' ').sum(axis=1)

for i in range(df2.shape[0]):
    if pd.isna(df2['description'][i])==True :
        df2['description'][i] = 'No description'
df2['Combined'] = df2.fillna(' ').sum(axis=1)

#выравнивание регистра, удаление цифр, знаков препинания, разметки страницы
df1['Combined']= df1['Combined'].map(lambda x: x.lower())
for i in range(df1.shape[0]):
    df1['Combined'][i]=str(clean_tweet(df1['Combined'][i]))
    #print('{})'.format(i) + df1['description'][i])
    #print('\n')

df1['Combined'] = df1['Combined'].astype(str)

stop_words = set(stopwords.words("english"))
stop_words1 = set(stopwords.words("russian"))

df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stop_words))
df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stop_words1))

#лемматизация русских слов
morph = pymorphy2.MorphAnalyzer()
df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(morph.parse(tok)[0].normal_form for tok in x))
stemmer = SnowballStemmer("russian") 
df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(stemmer.stem(k) for k in x ))
#стемминг английских
stemmer = SnowballStemmer("english") 
df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(stemmer.stem(k) for k in x ))

for i in range(df1.shape[0]):
    df1['Combined'][i]=str(clean_tweet(df1['Combined'][i]))

stop_words = set(stopwords.words("english"))
stop_words1 = set(stopwords.words("russian"))

df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stop_words))
df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stop_words1))

token = []
for i in range(df1.shape[0]):
    a=nltk.word_tokenize(df1['Combined'][i])
    token.append(nltk.word_tokenize(df1['Combined'][i]))

#TF-IDF
def compute_tfidf(corpus):
    def compute_tf(text):
        tf_text = Counter(text)
        for i in tf_text:
            tf_text[i] = 0.5 + (0.5 * (tf_text[i]/tf_text.most_common(1)[0][1]))
        return tf_text
    def compute_idf(word, corpus):
        return math.log10(1 + (len(corpus))/float(sum([1 for i in corpus if word in i])))

    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            tf_idf_dictionary[word] = computed_tf[word] * compute_idf(word, corpus)
        documents_list.append(tf_idf_dictionary)
    return documents_list

tf_idf = compute_tfidf(token)

new_tf_idf = [{k:v for k,v in tf_dict.items() if 1 < v < 1.7} for tf_dict in tf_idf]
for i in range(len(df1['Combined'])):
    word_list = df1['Combined'][i].split()
    tmp = ''
    for word in word_list:
        if word in new_tf_idf[i]:
            tmp+= word + ' '
    df2['Combined'][i] = tmp

token = []
for i in range(df1.shape[0]):
    a=nltk.word_tokenize(df2['Combined'][i])
    token.append(nltk.word_tokenize(df2['Combined'][i]))

dct = corpora.Dictionary([df2['Combined'][0].split()])
for i in range(df1.shape[0]):
    dct.add_documents([df2['Combined'][i].split()])  
corpus = [ dct.doc2bow(doc, allow_update=True) for doc in token]

from gensim.models import LdaModel, LdaMulticore

lda_model = LdaMulticore(corpus=corpus,
                         id2word=dct,
                         random_state=100,
                         num_topics=18,
                         passes=10,
                         chunksize=1000,
                         batch=False,
                         alpha='asymmetric',
                         decay=0.5,
                         offset=64,
                         eta=None,
                         eval_every=0,
                         iterations=100,
                         gamma_threshold=0.001,
                         per_word_topics=True)

lda_model.print_topics(-1)
