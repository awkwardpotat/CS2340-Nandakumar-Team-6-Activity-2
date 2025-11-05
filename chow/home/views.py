from django.shortcuts import render, redirect
from restaurants.models import Restaurant, Review
from accounts.models import User
# Create your views here.
def home(request):
    context = {
        'featured_restaurants': Restaurant.objects.order_by('-average_rating')[:3],
        'restaurant_count': Restaurant.objects.count(),
        'review_count': Review.objects.count(),
        'user_count': User.objects.count()
    }
    return render(request, 'home/home.html', context)

def favorites(request):
    if not request.user.is_authenticated:
        return redirect('accounts.login')
    restaurants = request.user.favorite_restaurants.all()
    return render(request, 'home/favorites.html', {'restaurants': restaurants})

