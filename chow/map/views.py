from django.shortcuts import render

# Create your views here.
#MAP STUFF HERE
def show_map(request):
    return render(request, 'map/map.html')