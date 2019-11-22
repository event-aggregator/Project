from django.shortcuts import render, redirect
from django.contrib.auth import logout
from database.models import Client, Cities, Areas, Languages, ClientCities, ClientAreas, ClientLanguages
from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError


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

    context = {
        "user": user,
        "cities": all_cities,
        "areas": all_areas,
        "languages": all_langs
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
