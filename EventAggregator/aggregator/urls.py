
from django.urls import re_path, path
from . import views


urlpatterns = [
    re_path('hello', views.hello, name='hello'),
    re_path('okay', views.okay, name="okay"),

]