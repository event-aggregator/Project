#!/usr/bin/env python
# coding: utf-8

import pandas as pd
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

import json, requests
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

def timepad(url):
    data = pd.DataFrame(index=[], columns=[]).fillna(0) #Создание пустого dataframe
    skip=0 #Можно только по 100 страниц загружать, поэтому цикл, пока не придёт пустой ответ:
    while True:
        response = requests.get(url) #Получение ответа с сервера
        data_add=json_normalize(pd.DataFrame(response.json())['values'])#Ответ приходит кривой, полностью загруженный в значение values, нормализуем относительно values, переводим json в dataframe 
        if data_add.empty:
            break
        data=(pd.concat([data, data_add], ignore_index=True,sort=False))#Соединение с основным датафреймом данных ста страниц
        skip+=100
        url=url.replace('skip='+str(skip-100), 'skip='+str(skip))#Изменяю в запросе дать мне следующие 100 страниц
    #Переименование колонок и удаление всего ненужного:
    data.drop(['categories','description_short','moderation_status','organization.id','poster_image.default_url','organization.logo_image.uploadcare_url','organization.logo_image.default_url','organization.subdomain','organization.description_html', 'organization.url','location.coordinates'], axis=1, inplace=True)
    data=data.rename({'description_html': 'description','location.country' :'country','url': 'link', 'poster_image.uploadcare_url': 'image', 'location.city': 'city', 'location.address': 'address', 'organization.name': 'group_name'}, axis=1)
    date_time=data['starts_at'].str.split('T',expand=True) #Приведение колонок времени и даты в нужный вид:
    date_time.columns=['date','time']
    date_time.time=pd.Series(date_time['time']).str.replace(':00+0300', ' ',regex=False)
    data=(pd.concat([data, date_time],axis=1))
    data = data[data.country == 'Россия'] #Оставляю только мероприятия в России
    data.drop(['starts_at','country'],axis=1,inplace=True) #Удаление теперь ненужных колонок
    data.loc[data.city == 'Без города', 'city'] = 'Онлайн' #Всё, что без города - онлайн мероприятия
    return data

def meetup(url):
    data = pd.DataFrame(index=[], columns=[]).fillna(0)
    key=['791b24a3e1670f2651183c1c2e4c5c', '3d7f5d5049b117e74666395f306e43','264e2c412f705c562a2f304df55769','573f6f2839355971c476b6a294d1025','4b21301a37523464f4d395817dd36']
    city=['Санкт-Петербург','Москва','Новосибирск','Екатеринбург','Нижний Новгород']
    for i in range(len(key)): 
        response = requests.get(url, params={'key': key[i]}) #Получение ответа с каждым из токенов
        data_add=json.dumps(response.json()) #Преобазование json в строку
        data_add="{"+data_add[data_add.find('}')+2:] #Ответ приходит весьма необычным, поэтому так надо :D
        data_add=json_normalize(pd.DataFrame(json.loads(data_add))['events']) #Преобразование обратно в json, перевод в датафрейм, нормализуем
        data_add=data_add.rename({'venue.city':'city'}, axis=1) #Переименовываем колонку, чтобы без точки была 
        data_add.city=city[i] 
        data=(pd.concat([data, data_add], ignore_index=True,sort=False)) #Соединение с основным датафреймом
    #Удаляем ненужное, переименовываем:
    data=data[['id','name','local_date', 'local_time','city','status','link', 'description', 'group.name','visibility','group.urlname','venue.address_1', 'venue.address_2','venue.name']]
    data=data.rename({'group.name': 'group_name','group.urlname':'urlname','local_date': 'date','local_time': 'time','status':'address','visibility':'image'}, axis=1)
    data.address=data.apply(lambda x: f"{x['venue.address_1']} {x['venue.address_2']} {x['venue.name']}", axis=1) #Приходит аж 3 колонки с адресом, соединям их
    data.drop(['venue.address_1','venue.address_2','venue.name'], axis=1, inplace=True) #Удаляем то, что соединили
    data.address=pd.Series(data['address']).str.replace('nan', ' ',regex=False)
    for urlname in data.urlname: #Картиночки
        url_image= 'https://api.meetup.com/'+urlname+'/photos?&sign=true&photo-host=public&page=2'
        response=requests.get(url_image).json()
        if len(response)==2:
            data.loc[data.urlname==urlname,'image']=response[1]["highres_link"]
        else:
            data.drop(data[data.urlname==urlname].index,axis=0, inplace=True)
    data.drop(['urlname'], axis=1, inplace=True)
    return data

def get_dataframe():
    url_timepad='https://api.timepad.ru/v1/events?fields=description_short%2C%20description_html%2Clocation%2C%20organization&limit=100&skip=0&category_ids=452&access_statuses=public&moderation_statuses=featured%2C%20shown'
    url_meetup='https://api.meetup.com/find/upcoming_events?&sign=true&photo-host=public&topic_category=34&page=1000&allMeetups=true'
    data=(pd.concat([meetup(url_meetup),timepad(url_timepad)], ignore_index=True,sort=False))
    return data
    

def parser():
    data=get_dataframe()
    data_json=data.to_json(force_ascii=False)
    return data_json

def cities():
    city=[]
    url_timepad='https://api.timepad.ru/v1/events?fields=description_short%2C%20description_html%2Clocation%2C%20organization&limit=100&skip=0&category_ids=452&access_statuses=public&moderation_statuses=featured%2C%20shown'
    url_meetup='https://api.meetup.com/find/upcoming_events?&sign=true&photo-host=public&topic_category=34&page=1000&allMeetups=true'
    data=(pd.concat([meetup(url_meetup),timepad(url_timepad)], ignore_index=True,sort=False))
    for element in data.city:
        if element not in city:
            city.append(element)
    city.remove('Онлайн')
    return city
                            
                            
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
