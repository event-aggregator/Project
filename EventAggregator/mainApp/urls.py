from django.urls import path
from . import views

urlpatterns = [
    path('success', views.success),
    path('logout', views.out),
    path('faq', views.faq),
    path('feedback', views.feedback),
    path('user_page', views.user_page),
    path('cities', views.cities),
    path('contact', views.contact),

]