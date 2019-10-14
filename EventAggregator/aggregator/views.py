from django.shortcuts import render
from django.http import HttpResponse
from .models import Users


def hello(request):
    return render(request, 'index.html')

def okay(request):
    if request.method == "POST":
        user = request.POST['login']
        password = request.POST['password']
    Users.objects.create(
        login = user,
        password = password
    )


    return HttpResponse(a)
# Create your views here.
