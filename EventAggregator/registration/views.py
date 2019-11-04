from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from database.models import Client as User


def index(request):
    return render(request, 'registration/autho.html')


def gologin(request):
    return render(request, 'registration/autho.html')


def goregister(request):
    return render(request, 'registration/registration.html')


def register(request):
    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password.decode('utf-8'), email=request.POST['email'])
    user.save()
    request.session['email'] = user.email
    return redirect('/success')


def login(request):
    error = ''
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']).exists():
            user = User.objects.filter(email=request.POST['email'])[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['email'] = user.email
                response = redirect('/success')
                return response
            else:
                error = u'Неверно введен пароль. Попробуйте снова.'
                context = {
                    "error": error
                }
        else:
            error = u'Такого логина не существует. Зарегистрируйтесь.'
            context = {
                "error": error
            }
        return render(request, 'registration/autho.html', context)


def success(request):
    user = User.objects.get(email=request.session['email'])
    context = {
        "user": user
    }
    return render(request, 'registration/success.html', context)