from django.shortcuts import render, redirect
from django.contrib.auth import logout
from database.models import Client, Cities, ClientCities
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
    print(cities)
    all_cities = []
    for city in cities:

        #создаем словарь
        city_info = {
            'city': city.city_name,
        }
        all_cities.append(city_info)

    context = {
        "user": user,
        "cities": all_cities
    }
    return render(request, 'mainApp/user_page.html', context)

def cities(request):
    # user = Client.objects.filter(email=request.session['email']).first()
    # for i in request.POST.getlist('cities'):
    #     city = Cities.objects.filter(name=i).first()
    #     user.cities.add(city)
    #     user.save()
    # return redirect('/user_page')
    user = Client.objects.filter(email=request.session['email']).first()
    for i in request.POST.getlist('cities'):
        city = Cities.objects.filter(name=i).first()
        city1 = ClientCities(user_email=user, city_name=city)
        city1.save()
    return redirect('/user_page')


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
