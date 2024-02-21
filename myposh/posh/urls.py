from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage.as_view(), name='index')
    
]