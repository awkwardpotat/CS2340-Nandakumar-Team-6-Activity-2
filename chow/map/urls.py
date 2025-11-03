from django.urls import path
from . import views
urlpatterns = [
    path('', views.show_map, name='map.show_map'),
]