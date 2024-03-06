from django.shortcuts import render
from django.views import View

def home(request):
    return render(request, 'home.html', {})

def register(request):
    return render(request, 'register.html', {})