from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home" ),
    path('register/', views.register, name="register"),
    path('register/ngo/', views.register_ngo, name="register_ngo"),
    path('register/consultancy/', views.register_consultancy, name="register_consultancy"),
    path('register/establishment/', views.register_establishment, name="register_establishment"),
    path('login/', views.signin, name="login"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.signout, name="logout"),
    # path('register/otp/', views.otp, name="otp"),
    path('index/', views.index, name='tp'),
]