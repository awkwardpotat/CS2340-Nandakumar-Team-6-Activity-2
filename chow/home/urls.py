from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home.home'),
    path('favorites/', views.favorites, name='home.favorites')
]