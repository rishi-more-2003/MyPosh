from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home" ),

    path('page/', views.page, name='page'),
    path('visibility/', views.visibility, name='visibility'),

    path('register/', views.register, name="register"),
    path('register/ngo/', views.register_ngo, name="register_ngo"),
    path('register/consultancy/', views.register_consultancy, name="register_consultancy"),
    path('register/establishment/', views.register_establishment, name="register_establishment"),
    path('login/', views.signin, name="login"),

    path('profile/', views.profile, name="profile"),
    path('logout/', views.signout, name="logout"),

    path('profile/education/create', views.education, name="education"),
    path('profile/education/delete/<int:pk>', views.delete_education, name="delete_education"),
    path('profile/education/edit/<int:pk>/', views.edit_education, name="edit_education"),

    path('profile/service/create', views.service, name="service"),
    path('profile/service/delete/<int:pk>', views.delete_service, name="delete_service"),
    path('profile/service/edit/<int:pk>/', views.edit_service, name="edit_service"),

    path('ngo-profile/service/create', views.ngo_service, name="ngo_service"),
    path('ngo-profile/service/delete/<int:pk>', views.ngo_delete_service, name="ngo_delete_service"),
    path('ngo-profile/service/edit/<int:pk>/', views.ngo_edit_service, name="ngo_edit_service"),

    path('consult-profile/service/create', views.consult_service, name="consult_service"),
    path('consult-profile/service/delete/<int:pk>', views.consult_delete_service, name="consult_delete_service"),
    path('consult-profile/service/edit/<int:pk>/', views.consult_edit_service, name="consult_edit_service"),

    path('profile/experience/create', views.experience, name="experience"),
    path('profile/experience/delete/<int:pk>', views.delete_experience, name="delete_experience"),
    path('profile/experience/edit/<int:pk>/', views.edit_experience, name="edit_experience"),

    path('ngo-profile/experience/create', views.ngo_experience, name="ngo_experience"),
    path('ngo-profile/experience/delete/<int:pk>', views.ngo_delete_experience, name="ngo_delete_experience"),
    path('ngo-profile/experience/edit/<int:pk>/', views.ngo_edit_experience, name="ngo_edit_experience"),

    path('consult-profile/experience/create', views.consult_experience, name="consult_experience"),
    path('consult-profile/experience/delete/<int:pk>', views.consult_delete_experience, name="consult_delete_experience"),
    path('consult-profile/experience/edit/<int:pk>/', views.consult_edit_experience, name="consult_edit_experience"),

    path('profile/certification/create', views.certification, name="certification"),
    path('profile/certification/delete/<int:pk>', views.delete_certification, name="delete_certification"),
    path('profile/certification/edit/<int:pk>/', views.edit_certification, name="edit_certification"),

    path('profile/skill/create', views.skill, name="skill"),
    path('profile/skill/delete/<int:pk>', views.delete_skill, name="delete_skill"),
    path('profile/skill/edit/<int:pk>/', views.edit_skill, name="edit_skill"),

    path('profile/comittee/<int:pk>', views.delete_comitteeuid, name="comittee_uid"),
    path('ngo-profile/comittee/<int:pk>', views.delete_ngocomitteeuid, name="comittee_ngo_uid"),
    path('consult-profile/comittee/<int:pk>', views.delete_consultcomitteeuid, name="comittee_consult_uid"),

    path('profile/client/<int:pk>', views.delete_clientname, name="client_name"),
    path('ngo-profile/client/<int:pk>', views.delete_ngoclientname, name="client_ngo_name"),
    path('consult-profile/client/<int:pk>', views.delete_consultclientname, name="client_consult_name"),

    path('ngo-profile/member/<int:pk>', views.delete_ngomember, name="ngo_member"),
    path('consult-profile/member/<int:pk>', views.delete_consultmember, name="consult_member"),

    path('ngo-profile/', views.ngo_profile, name="ngo-profile"),
    path('ngo-profile/document/<int:pk>', views.delete_document, name="delete_document"),

    path('consult-profile/', views.consult_profile, name="consult-profile"),
    path('consult-profile/document/<int:pk>', views.consult_delete_document, name="consult_delete_document"),


    path('portal/', views.portal, name="portal"),
    path('user-list/', views.list_user, name="list_user"),
    path('user-details/<str:pk>/', views.user_details, name="user_details"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)