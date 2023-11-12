from django.urls import path
from . import views
from .views import index, pokemon_detail

urlpatterns = [
    path('', views.index, name='index'),
    path('pokemon-detail/<int:pokemon_id>/', pokemon_detail, name='pokemon_detail'),
]
