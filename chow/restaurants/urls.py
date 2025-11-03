from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='restaurants.index'),
    path('<int:id>/', views.show, name='restaurants.show'),
    path('<int:id>/review/create/', views.create_review, name='restaurants.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='restaurants.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='restaurants.delete_review'),
]