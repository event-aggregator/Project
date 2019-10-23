from django.shortcuts import render, redirect
from django.contrib.auth import logout
from database.models import Client as User


def success(request):
    user = User.objects.get(email=request.session['email'])
    return render(request, 'mainApp/main.html')


def out(request):
    logout(request)
    return redirect('/gologin')


def faq(request):
    user = User.objects.get(email=request.session['email'])
    return render(request, 'mainApp/faq.html')


def feedback(request):
    user = User.objects.get(email=request.session['email'])
    return render(request, 'mainApp/feedback.html')
