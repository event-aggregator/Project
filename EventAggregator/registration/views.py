from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from database.models import Client as User
from database.models import Cities, ClientCities, Areas, ClientAreas, Languages, ClientLanguages


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
    return redirect('/afterReg')


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


def interests(request):
    # user = Client.objects.filter(email=request.session['email']).first()
    # for i in request.POST.getlist('cities'):
    #     city = Cities.objects.filter(name=i).first()
    #     user.cities.add(city)
    #     user.save()
    # return redirect('/user_page')
    user = User.objects.filter(email=request.session['email']).first()

    for i in request.POST.getlist('cities'):
        city = Cities.objects.filter(id=i).first()
        if not ClientCities.objects.filter(user_email=user, city_id=city).exists():
            city1 = ClientCities(user_email=user, city_id=city)
            city1.save()

    print(request.POST)
    for i in request.POST.getlist('areas'):
        area = Areas.objects.filter(id=i).first()
        print(i)
        print(area)
        print(user)
        if not ClientAreas.objects.filter(user_email=user, area_id=area).exists():
            area1 = ClientAreas(user_email=user, area_id=area)
            area1.save()

    for i in request.POST.getlist('languages'):
        language = Languages.objects.filter(id=i).first()
        if not ClientLanguages.objects.filter(user_email=user, language_id=language).exists():
            lang1 = ClientLanguages(user_email=user, language_id=language)
            lang1.save()
    return redirect('/success')


def afterReg(request):

    languages = Languages.objects.all()
    areas = Areas.objects.all()
    cities = Cities.objects.all()
    all_lang = []
    all_areas = []
    all_cities = []

    for lang in languages:
        lang_info = {
            'id': lang.id,
            'name': lang.name,
        }
        all_lang.append(lang_info)

    for city in cities:
        city_info = {
            'id': city.id,
            'name': city.name,
        }
        all_cities.append(city_info)

    for area in areas:
        area_info = {
            'name': area.name,
            'id': area.id,
        }
        all_areas.append(area_info)

    context = {
        'languages': all_lang,
        'areas': all_areas,
        'cities': all_cities,
    }

    return render(request, 'registration/afterReg.html', context)
