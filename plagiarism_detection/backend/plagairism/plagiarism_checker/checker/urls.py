# checker/urls.py
from .views import *

from django.urls import path
from .views import check_plagiarism

urlpatterns = [
    path('', home, name='home'),
    path('about',about,name="about"),
    path('check', check_plagiarism, name='check_plagiarism'),
    path('registration',registration,name="regi"),
    path("login",login,name="login")
]