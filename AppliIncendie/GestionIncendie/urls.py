from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_accueil, name='accueil'),
    path('map', views.map, name='map'),
    path('detail_global', views.details_dref),
    path('detail_dp/<id_dp>', views.details_dp, name='details_dp'),
    path('detail_ccdrf/<id_ccdrf>', views.details_ccdrf, name='details_ccdrf'),
    path('detail_sf/<id_sf>', views.details_sf, name='sf'),
]