import json, requests
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

url='https://api.timepad.ru/v1/events?fields=description_short%2C%20description_html%2Clocation%2C%20organization&limit=100&skip=0&category_ids=452&access_statuses=public&moderation_statuses=featured%2C%20shown'
url2='https://api.meetup.com/find/upcoming_events?&sign=true&photo-host=public&topic_category=34&page=1000&allMeetups=true'
data = pd.DataFrame(index=[], columns=[]).fillna(0)
data_timepad,data_meetup=data,data

#timepad:
skip=0
while True:
    response = requests.get(url)
    data_add=json_normalize(pd.DataFrame(response.json())['values'])
    if data_add.empty:
        break
    data_timepad=(pd.concat([data_timepad, data_add], ignore_index=True,sort=False))
    skip+=100
    url=url.replace('skip='+str(skip-100), 'skip='+str(skip))
data_timepad.drop(['categories','description_short','moderation_status','organization.id','poster_image.default_url','organization.logo_image.uploadcare_url','organization.subdomain','organization.description_html', 'organization.url','location.coordinates'], axis=1, inplace=True)
data_timepad=data_timepad.rename({'description_html': 'description','location.country' :'country','url': 'link', 'poster_image.uploadcare_url': 'image', 'location.city': 'city', 'location.address': 'address', 'organization.name': 'group_name','organization.logo_image.default_url':'group_image'}, axis=1)
date_time=data_timepad['starts_at'].str.split('T',expand=True)
date_time.columns=['date','time']
date_time.time=pd.Series(date_time['time']).str.replace(':00+0300', ' ',regex=False)
data_timepad=(pd.concat([data_timepad, date_time],axis=1))
data_timepad = data_timepad[data_timepad.country == 'Россия']
data_timepad.drop(['starts_at','country'],axis=1,inplace=True)
data_timepad.loc[data_timepad.city == 'Без города', 'city'] = 'Онлайн'

#meetup:
key=['791b24a3e1670f2651183c1c2e4c5c', '3d7f5d5049b117e74666395f306e43','264e2c412f705c562a2f304df55769','573f6f2839355971c476b6a294d1025','4b21301a37523464f4d395817dd36']
city=['Санкт-Петербург','Москва','Новосибирск','Екатеринбург','Нижний Новгород']
for i in range(len(key)):
    response = requests.get(url2, params={'key': key[i]})
    data_add=json.dumps(response.json())
    data_add="{"+data_add[data_add.find('}')+2:]
    data_add=json_normalize(pd.DataFrame(json.loads(data_add))['events'])
    data_add=data_add.rename({'venue.city':'city'}, axis=1)
    data_add.city=city[i]
    data_meetup=(pd.concat([data_meetup, data_add], ignore_index=True,sort=False))
data_meetup.drop(['created','duration','date_in_series_pattern','time','updated','utc_offset', 'waitlist_count', 'yes_rsvp_count','visibility','venue.lon','venue.lat','member_pay_fee', 'group.created','group.id','group.join_mode', 'group.lat', 'group.lon','group.who', 'group.localized_location', 'group.state', 'group.country','group.region', 'group.timezone', 'rsvp_limit', 'pro_is_email_shared','venue.id','venue.repinned','venue.country','venue.localized_country_name','how_to_find_us', 'fee.accepts','fee.amount', 'fee.currency','fee.description', 'fee.label','fee.required', 'rsvp_close_offset'], axis=1, inplace=True)
data_meetup=data_meetup.rename({'group.name': 'group_name','local_date': 'date','local_time': 'time','status':'address'}, axis=1)
data_meetup.address=data_meetup.apply(lambda x: f"{x['venue.address_1']} {x['venue.address_2']} {x['venue.name']}", axis=1)
data_meetup.drop(['venue.address_1','venue.address_2','venue.name','rsvp_open_offset', 'venue.phone'], axis=1, inplace=True)
data_meetup.address=pd.Series(data_meetup['address']).str.replace('nan', ' ',regex=False)

data=(pd.concat([data_meetup, data_timepad], ignore_index=True,sort=False))
print(data.city)

writer = pd.ExcelWriter('C:\\Users\\Dasha\\Desktop\\study\\python\\analys\\Data.xlsx', engine='xlsxwriter')
data.to_excel(writer, 'Events')
writer.save()
# xl_file = pd.ExcelFile('C:\\Users\\Dasha\\Desktop\\study\\python\\analys\\Data.xlsx')
# df = xl_file.parse('Events')


# import psycopg2  
# conn = psycopg2.connect(dbname='my_database', user='username')
# cursor = conn.cursor() 

# # Выполняем запрос.
# cursor.execute("SELECT * FROM table_name")
# row = cursor.fetchone()
 
# # Закрываем подключение.
# cursor.close()
# conn.close()