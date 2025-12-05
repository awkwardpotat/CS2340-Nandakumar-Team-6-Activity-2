from django.shortcuts import render
from django.http import JsonResponse
from restaurants.models import Restaurant
import json

# Create your views here.
#MAP STUFF HERE
def show_map(request):
    # Get all restaurants with coordinates
    restaurants = Restaurant.objects.filter(latitude__isnull=False, longitude__isnull=False).values(
        'id', 'name', 'latitude', 'longitude', 'average_rating'
    )
    restaurants_json = json.dumps(list(restaurants))
    context = {
        'restaurants_json': restaurants_json,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'map/map.html', context)