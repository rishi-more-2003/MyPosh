from django.urls import path 
from . import views 

app_name = "conversation"

urlpatterns = [
    path('new/<int:pk>/', views.new_conversation, name="new"),
    path('', views.inbox, name="inbox"),
]