from django.shortcuts import render, redirect
from django.contrib.auth import logout
from database.models import Client, Cities, Areas, Languages, ClientCities, ClientAreas, ClientLanguages, Events, Cities, EventCities, ClientEvents
from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from .gets import parser, cities
import json
from .Claster import clast


def success(request):
    user = Client.objects.get(email=request.session['email'])
    return render(request, 'mainApp/main.html')


def out(request):
    logout(request)
    return redirect('/gologin')


def faq(request):
    user = Client.objects.get(email=request.session['email'])
    return render(request, 'mainApp/faq.html')


def feedback(request):
    user = Client.objects.get(email=request.session['email'])
    return render(request, 'mainApp/feedback.html')

def user_page(request):
    user = Client.objects.get(email=request.session['email'])
    cities = ClientCities.objects.filter(user_email=user.email)
    all_cities = []
    for city in cities:
        city1 = Cities.objects.filter(id=city.city_id_id).first()
        city_info = {
            'name': city1.name,
        }
        all_cities.append(city_info)

    areas = ClientAreas.objects.filter(user_email=user.email)
    all_areas = []
    for area in areas:
        area1 = Areas.objects.filter(id=area.area_id_id).first()
        area_info = {
            'name': area1.name,
        }
        all_areas.append(area_info)

    languages = ClientLanguages.objects.filter(user_email=user.email)
    all_langs = []
    for lang in languages:
        lang1 = Languages.objects.filter(id=lang.language_id_id).first()
        lang_info = {
            'name': lang1.name,
        }
        all_langs.append(lang_info)

    events = ClientEvents.objects.filter(user_email=user.email, status=True)
    all_events = []
    for event in events:
        event1 = Events.objects.filter(id=event.events_id_id).first()
        event_info = {
            'name': event1.name,
            'date': event1.date,
            'link': event1.link
        }
        all_events.append(event_info)

    context = {
        "user": user,
        "cities": all_cities,
        "areas": all_areas,
        "languages": all_langs,
        'events': all_events
    }
    return render(request, 'mainApp/user_page.html', context)


def contact(request):
    user = Client.objects.get(email=request.session['email'])
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            recepients = ['event_aggregator@mail.ru']
            # Если пользователь захотел получить копию себе, добавляем его в список получателей
            message += "\n" + "От: " + user.email

            try:
                send_mail(subject, message, 'event_aggregator@mail.ru', recepients)
            except BadHeaderError: #Защита от уязвимости
                return HttpResponse('Invalid header found')
            # Переходим на другую страницу, если сообщение отправлено
            return render(request, 'mainApp/thanks.html')

    else:
        form = ContactForm()
    # Выводим форму в шаблон
    return render(request, 'mainApp/feedback.html', {'form': form, 'username': user.first_name})


def import_events(request):
    #a = parser()
    #
    # with open('data.json', 'w') as f:
    #     json.dump(a, f, ensure_ascii=False)
    # city_all = cities()
    # print(city_all)
    #
    # for j in city_all:
    #     city = Cities.objects.create(name=j)
    #     city.save()

    with open('data.json', 'r') as f:
        data = json.load(f)
    for i in data['events']:
        id = i['id']
        name = i['name']
        city = i['city']
        print(city)
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

        if Cities.objects.filter(name=city).exists():
            city = Cities.objects.filter(name=city).first()
            if not EventCities.objects.filter(event_id_id=id, city_id_id=city.id).exists():
                city1 = EventCities(event_id_id=id, city_id_id=city.id)
                city1.save()
    return 'OK'


def swipe(request):
    user = Client.objects.get(email=request.session['email'])
    areas = ClientAreas.objects.filter(user_email=user.email)
    all_areas = []
    for area in areas:
        area1 = Areas.objects.filter(id=area.area_id_id).first()
        all_areas.append(area1.name)

    languages = ClientLanguages.objects.filter(user_email=user.email)
    for lang in languages:
        lang1 = Languages.objects.filter(id=lang.language_id_id).first()

        all_areas.append(lang1.name)
    number = clast(all_areas)

    events = Events.objects.filter(theme=number)[:10]
    all_events = []
    for event in events:
        event_info = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date,
            'image': event.image,
            'link': event.link
        }
        all_events.append(event_info)

    context = {
        'events': all_events
    }
    return render(request, 'mainApp/swipe.html', context)



@csrf_exempt
def abc(request):
    user = Client.objects.get(email=request.session['email'])
    a = request.POST.keys()
    a = list(a)[0].replace('{','').replace('}','').replace(':', ' ').replace(',', ' ').replace('"','').split()
    print(a)

    if a[3] == 'true':
        k = True
    else:
        k = False

    event = Events.objects.filter(id=a[1]).first()
    if not ClientEvents.objects.filter(user_email=user, events_id=event).exists():
        event1 = ClientEvents(user_email=user, events_id=event, status=k)
        event1.save()


    return render(request, 'mainApp/feedback.html')



