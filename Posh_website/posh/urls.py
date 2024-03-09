from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home" ),
    path('register/', views.register, name="register"),
    path('login/', views.signin, name="login"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.signout, name="logout"),
    path('register/otp/', views.otp, name="otp"),
]