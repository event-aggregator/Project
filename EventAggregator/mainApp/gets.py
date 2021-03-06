import json, requests
import pandas as pd
import re
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
    data.image=pd.Series(data['image']).str.replace('//',' ',regex=False)
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
    for urlname in data.urlname: #Картиночки
        url_image= 'https://api.meetup.com/'+urlname+'/photos?&sign=true&photo-host=public&page=2'
        response=requests.get(url_image).json()
        if len(response)==2:
            data.loc[data.urlname==urlname,'image']=response[1]["highres_link"]
        else:
            data.drop(data[data.urlname==urlname].index,axis=0, inplace=True)
    data.drop(['urlname'], axis=1, inplace=True)
    return data

def clean_tweet(tweet):
    if pd.isna(tweet)==False :
        tweet = re.sub('href\S+\s*', '', tweet)
        tweet = re.sub('www\s*', '', tweet)
        tweet = re.sub('http\S+\s*', '', tweet) 
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
        tweet = re.sub('@\S+', '', tweet)
        tweet = re.sub('style|text|align| scr |justify| с | pm |gdg| sb |rte|width|font|—| gc |size|bgcolor|dcdcdc|rsvp|height| alt | px | src |colspan| st | spb |class| gt | lt | br | p |center|left', ' ', tweet)
    return tweet 

def get_dataframe():
    url_timepad='https://api.timepad.ru/v1/events?fields=description_short%2C%20description_html%2Clocation%2C%20organization&limit=100&skip=0&category_ids=452&access_statuses=public&moderation_statuses=featured%2C%20shown'
    url_meetup='https://api.meetup.com/find/upcoming_events?&sign=true&photo-host=public&topic_category=34&page=1000&allMeetups=true'
    data=(pd.concat([meetup(url_meetup),timepad(url_timepad)], ignore_index=True,sort=False))
    data.address=pd.Series(data['address']).str.replace('nan', ' ',regex=False)
    data.fillna(' ',inplace=True) 
    data=data.T
    for i in range(len(data.columns)):
        data.loc['description',i] = clean_tweet(data.loc['description',i])
    return data

def parser():
    data=get_dataframe()
    events=[]
    for i in range(len(data.columns)):
        events.append(data[i].to_dict())
    data_json= {'events':events}
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

def import_events():
    a = parser()

    with open('data.json', 'w') as f:
        json.dump(a, f, ensure_ascii=False)

    with open('data.json', 'r') as f:
        data = json.load(f)
    for i in data['events']:
        id = i['id']
        name = i['name']
        city = i['city']
        date = i['date']
        description = i['description']
        address = i['address']
        link = i['link']
        image = i['image']

        if not Events.objects.filter(id=id).exists():
            event = Events.objects.create(id=id, name=name, date=date,
                                          description=description, address=address,
                                          link=link, image=image)
            event.save()
            print(event)
        city = Cities.objects.filter(name=city).first()
        print(city)
        if city != []:
            if not EventCities.objects.filter(event_id_id=id, city_id_id=city[0]).exists():
                city1 = EventCities(event_id_id=id, city_id=city[0])
                city1.save()