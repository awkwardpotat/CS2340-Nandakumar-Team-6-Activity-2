from django import forms
from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'description',
            'price_range',
            'image',
            'city',
            'state',
            'country',
            'location',
            'latitude',
            'longitude',
        ]
        widgets = {
            # latitude/longitude are handled via the map and should be hidden from the user
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            # hide the resolved address components; show the combined `location` instead
            'city': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'country': forms.HiddenInput(),
        }
