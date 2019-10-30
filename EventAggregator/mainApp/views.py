from django.shortcuts import render, redirect
from django.contrib.auth import logout
from database.models import Client, Cities
from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect


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
    print(user)
    context = {
        "user": user,
    }
    return render(request, 'mainApp/user_page.html', context)

def cities(request):
    user = Client.objects.filter(email=request.session['email']).first()

    for i in request.POST.getlist('cities'):
        city = Cities.objects.filter(name=i).first()
        user.cities.add(city)

        user.save()

    return redirect('/user_page')


# def contactform(reguest):
#     if reguest.method == 'POST':
#         form = ContactForm(reguest.POST)
#         # Если форма заполнена корректно, сохраняем все введённые пользователем значения
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             sender = form.cleaned_data['sender']
#             message = form.cleaned_data['message']
#             copy = form.cleaned_data['copy']
#
#             recepients = ['myemail@gmail.com']
#             # Если пользователь захотел получить копию себе, добавляем его в список получателей
#             if copy:
#                 recepients.append(sender)
#             try:
#                 send_mail(subject, message, 'myemail@gmail.com', recepients)
#             except BadHeaderError: #Защита от уязвимости
#                 return HttpResponse('Invalid header found')
#             # Переходим на другую страницу, если сообщение отправлено
#             return HttpResponseRedirect('/blog/thanks/')
#
#     else:
#         form = ContactForm()
#     # Выводим форму в шаблон
#     return render(reguest, 'contact.html', {'form': form, 'username': auth.get_user(reguest).username})
