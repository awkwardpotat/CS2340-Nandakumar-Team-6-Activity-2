from django.db import models
from django.contrib.auth.models import User
from accounts.models import Owner, Reviewer

# Create your models here.
#restaurant and reviews here
class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    average_rating = models.DecimalField(decimal_places=2, max_digits = 3, null=True, blank=True)
    description = models.CharField(max_length=255)
    # to filter: Restaurant.objects.filter(owner = [OWNER ID HERE])]
    # Set this value when creating a restaurant. Creating user might be deleted, so allow blank and don't cascade.
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True) 
    # ask if the user is the owner of the restaurant they are creating. If not, leave null.
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True) 
    favorites = models.ManyToManyField(User, blank=True, related_name='favorite_restaurants')
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)

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
            self.average_rating = None
        self.save()

    def get_gallery(self):
        """Return gallery images ordered by their `order` field."""
        return self.images.all()

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

class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"Reply by {self.author_user.username} on review {self.review.id}"

    def is_owner_reply(self):
        """Check if this reply was written by the restaurant owner"""
        try:
            owner = Owner.objects.get(user=self.author_user)
            return self.review.restaurant.owner == owner
        except Owner.DoesNotExist:
            return False


class RestaurantImage(models.Model):
    """Gallery image for a Restaurant.

    Use `restaurant.images` (related_name) to access the gallery.
    """
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='restaurant_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image {self.id} for {self.restaurant.name}"