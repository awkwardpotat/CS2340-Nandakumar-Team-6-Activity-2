from django.contrib import admin
from .models import Restaurant, Review, ReviewReply, RestaurantImage
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(RestaurantImage)