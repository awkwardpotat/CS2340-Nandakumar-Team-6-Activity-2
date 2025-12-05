from django.shortcuts import render
from django.http import JsonResponse
from restaurants.models import Restaurant
import json
from decimal import Decimal

# Create your views here.
#MAP STUFF HERE
def show_map(request):
    # Get all restaurants with coordinates
    restaurants = Restaurant.objects.filter(latitude__isnull=False, longitude__isnull=False).values(
        'id', 'name', 'latitude', 'longitude', 'average_rating', 'price_range'
    )
    # Ensure Decimal fields are converted to JSON-serializable types
    restaurant_list = []
    for r in list(restaurants):
        avg = r.get('average_rating')
        if isinstance(avg, Decimal):
            r['average_rating'] = float(avg)
        restaurant_list.append(r)
    restaurants_json = json.dumps(restaurant_list)
    context = {
        'restaurants_json': restaurants_json,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'map/map.html', context)