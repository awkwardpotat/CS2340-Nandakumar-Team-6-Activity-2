from django.db import models
from django.contrib.auth.models import User
from accounts.models import Owner, Reviewer

# Create your models here.
#restaurant and reviews here
class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    average_rating = models.DecimalField(decimal_places=2, max_digits = 3)
    description = models.CharField(max_length=255)
    # to filter: Restaurant.objects.filter(owner = [OWNER ID HERE])
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    favorites = models.ManyToManyField(User, blank=True, related_name='favorite_restaurants')
    
    #LOCATION DATA
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    #text ver of location!!
    location = models.CharField(max_length=255, blank=True)
    #price range
    PRICE_RANGES = [
        ('cheap', '$'),
        ('medium', '$$'),
        ('pricey', '$$$'),
    ]
    price_range = models.CharField(max_length=10, choices=PRICE_RANGES, default='medium')

    def update_average_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            self.average_rating = total / reviews.count()
        else:
            self.average_rating = 0
        self.save()
    
    #image gallery how??

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.DecimalField(decimal_places=2, max_digits=3) #how many stars
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    #USER might mess things up vv
    # to filter: Review.objects.filter(user = [REVIEWER ID HERE])
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.restaurant.name