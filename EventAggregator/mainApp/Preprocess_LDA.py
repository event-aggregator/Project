#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re
import math
from .gets import get_dataframe
import json, requests
import nltk
from nltk import SnowballStemmer
from random import randint
from random import choice
from collections import Counter
from pandas.io.json import json_normalize
from sklearn.feature_extraction.text import CountVectorizer

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import LdaModel, LdaMulticore

# Plots
import pyLDAvis
import pyLDAvis.gensim  # don't skip thise

#nltk.download('punkt')



def format_dataset(df): 
    df = df.copy()
    df.drop(["id", "address","date","time","link","image","city"], axis = 1, inplace = True) 
    for i in range(df.shape[0]):
        if pd.isna(df['description'][i])==True :
            df['description'][i] = 'No description'
    df['Combined'] = df.fillna(' ').sum(axis=1)
    return(df)

def assignment_sw():
    with open('english_new.txt') as fe:
        stop_words = []
        for line in fe:
            new_line = re.sub(r'\s*\n','',line)
            stop_words.append(new_line)
    return stop_words    

def clean_tweet(tweet):
    if pd.isna(tweet)==False :
        tweet = re.sub('http\S*\s*', ' ', tweet) 
        tweet = re.sub('href\S+\s*', ' ', tweet)
        tweet = re.sub('www\s*', '', tweet)
        tweet = re.sub('\s\w\s', ' ', tweet)
        tweet = re.sub("\d+|-\d+", ' ',tweet)
        tweet = re.sub('<\w*\s\w+\W+\s*\w+\W+\w*\W*\w*\W+>', ' ', tweet)
        tweet = re.sub('</*\w*/*>*', ' ', tweet)
        tweet = re.sub('&\w+', ' ', tweet)
        tweet = re.sub('-end', 'end', tweet)
        tweet = re.sub('\W{2}', ' ', tweet)
        tweet = re.sub('\n', ' ', tweet)
        tweet = re.sub('\t', ' ', tweet) 
        tweet = re.sub('\xa0', ' ', tweet)
        tweet = re.sub('[а-яА-ЯёЁ]',' ', tweet) 
        tweet = re.sub('\[\w+\]',' ', tweet) 
        tweet = re.sub('•|//|\*|=+|↔|--|——| –| —| -| -',' ',tweet)
        tweet = re.sub('@\S+', ' ', tweet)
        tweet = re.sub('style|text|align| scr |justify| pm |gdg| sb |rte|er |or |width|font|—| gc |up |size|bgcolor|dcdcdc|rsvp|height| alt | px | src |colspan| st | spb |class| gt | lt | br | p |center|left', ' ', tweet)
        tweet = re.sub('[%s]' % re.escape("!''-""$%&()“”«»*╰,№./:;<=>✔✓®™?@[\]^_`{|}~📍🥳🚨🎢🏰👍🤙👌🚠🙆🤩🎤😶🤠🏨🀄🌾🚂🧗🏕🤡🌟🏃♻️😱🧠🚶 😋👇✨🕺💃🥂🏬🚩📆⏰🙂😉☕🧗📢💬😎❗✊🍿📌🤗🎁🌎🔥🦸‍♂️🦸‍♀️👩‍🚀✅👨‍🎨👨‍✈️👩‍✈️⚡🔋📱🕵🏻‍♂️📨🧳🤝👋🏼🎡😃💟🥏☝️🧾❤️💰🚀💡🤔👉🥒🌞🙍‍♂😊😌🗣☮💥🏠📝📞"), ' ', tweet) # удалит символы пунктуации
    return tweet 

def clean(df, stop_words):
    for i in range(df.shape[0]):
        df['Combined'][i]=str(clean_tweet(df['Combined'][i]))
    df['Combined'] = df['Combined'].astype(str) 
    df['Combined'] = df['Combined'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stop_words))
    return df

def data_preprocessing(df1):
    df1 = format_dataset(df)
    #выравнивание регистра, удаление цифр, знаков препинания, разметки страницы
    df1['Combined']= df1['Combined'].map(lambda x: x.lower())
    stop_words = assignment_sw() 
    df1 = clean(df1,stop_words)
    #стемминг английских
    stemmer = SnowballStemmer("english") 
    df1['Combined'] = df1['Combined'].str.split(' ').apply(lambda x: ' '.join(stemmer.stem(k) for k in x ))
    df1 = clean(df1,stop_words)
    return df1

def tf_idf(df1, df2):
    token = []
    for i in range(df1.shape[0]):
        token.append(nltk.word_tokenize(df1['Combined'][i]))
    #TF-IDF
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
        token.append(nltk.word_tokenize(df2['Combined'][i]))
    return df2, token

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

def LDA(corpus, dct, num):
    lda_model = LdaMulticore(corpus=corpus,
                         id2word=dct,
                         random_state=100,
                         num_topics=num,
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
    return lda_model

def opt_num(corpus,token,dct,num):    
    
    lda_model0 = LDA(corpus, dct, num)
    lda_model1 = LDA(corpus, dct, num-1)
    lda_model2 = LDA(corpus, dct, num+1)
    
    coherence_model_lda0 = CoherenceModel(model=lda_model0, texts=token, dictionary=dct, coherence='c_v')
    coherence0 = coherence_model_lda0.get_coherence()
    coherence_model_lda1 = CoherenceModel(model=lda_model1, texts=token, dictionary=dct, coherence='c_v')
    coherence1 = coherence_model_lda1.get_coherence()   
    coherence_model_lda2 = CoherenceModel(model=lda_model2, texts=token, dictionary=dct, coherence='c_v')
    coherence2 = coherence_model_lda2.get_coherence()    


    if ((coherence0 > coherence1)and(coherence0 > coherence2)):
        return lda_model0, num
    else: 
        if (coherence2 > coherence1):
            lda_model0, num = opt_num(corpus,token,dct,num+1)
            return lda_model0, num 
        else: 
            lda_model0, num = opt_num(corpus,token,dct,num-1)
            return lda_model0, num  

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()
    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row[0], key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

def analysis():
    df = get_dataframe()# тут должна быть функци получения датасета мероприятий из бд?
    df = df.T
    df1 = df.copy()
    df2 = df.copy()

    df2 = format_dataset(df2)
    df1 = data_preprocessing(df1)

    token = []
    df2, token = tf_idf(df1, df2)

    dct = corpora.Dictionary([df2['Combined'][0].split()])
    for i in range(df2.shape[0]):
        dct.add_documents([df2['Combined'][i].split()])  
    corpus = [ dct.doc2bow(doc, allow_update=True) for doc in token]
    num = 10
    lda_model, num = opt_num(corpus,token,dct,num)
    return lda_model, num, corpus,token


def mero_topick():
#соответствие номера мероприятия с номером темы
    lda_model, num, corpus,token = analysis()
    df_topic_sents_keywords = format_topics_sentences(lda_model, corpus, token)
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    df3=df_dominant_topic.copy()
    df3.drop(["Topic_Perc_Contrib","Keywords","Text"], axis = 1, inplace = True) #остается Document_No и Dominant_Topic
    df4 = df3.to_json(orient='values')
    return df4


def topick_key():
#соответствие номера темы с ключевыми словами
    lda_model, num, corpus,token = analysis()
    key = []
    for i in range (num):
        wp = lda_model.show_topic(i)
        topic_keywords = ", ".join([word for word, prop in wp])
        key.append(topic_keywords)
    d = pd.DataFrame()
    for i in range(num):
        d = d.append(pd.Series([i, key[i]]), ignore_index=True)         
    d.columns = ['num', 'Keywords']
    df5 = d.to_json(orient='values')
    return df5
