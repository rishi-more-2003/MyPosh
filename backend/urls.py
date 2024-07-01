from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('posh.urls')),
    path('inbox/', include('conversation.urls')),
    path('group/', include('group.urls')),
    path('', include('django.contrib.auth.urls')),
]
