from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_accueil, name='accueil'),
    path('map', views.map, name='map'),
]