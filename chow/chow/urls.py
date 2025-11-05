"""
URL configuration for chow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.models import User
from restaurants.models import Restaurant, Review

def home(request):
    context = {
        'featured_restaurants': Restaurant.objects.order_by('-average_rating')[:3],
        'restaurant_count': Restaurant.objects.count(),
        'review_count': Review.objects.count(),
        'user_count': User.objects.count()
    }
    return render(request, 'home.html', context)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('accounts/', include('accounts.urls')),
]
