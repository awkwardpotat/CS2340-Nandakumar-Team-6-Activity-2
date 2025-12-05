from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='restaurants.index'),
    path('create/', views.create_restaurant, name='restaurants.create'),
    path('<int:id>/', views.show, name='restaurants.show'),
    path('<int:id>/review/create/', views.create_review, name='restaurants.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='restaurants.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='restaurants.delete_review'),
    path('<int:id>/favorite/', views.toggle_favorite, name='restaurants.toggle_favorite'),
    path('<int:id>/claim/', views.toggle_claim, name='restaurants.toggle_claim'),
    path('restaurant/<int:id>/review/<int:review_id>/reply/', views.create_reply, name='restaurants.create_reply'),
    path('restaurant/<int:id>/review/<int:review_id>/reply/<int:reply_id>/delete/', views.delete_reply, name='restaurants.delete_reply'),
]