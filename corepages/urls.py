from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('administrator/', include('adminpages.urls')),
    path('headman/', include('headmanpages.urls')),
    path('teacher/', include('teacherpages.urls')),
]