from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#owner vs reviewer here?
#or owner is a more powerful reviewer?
#or anyone can be an owner?

# i think with one-to-one fields you can do both owner.user and user.owner
# https://docs.djangoproject.com/en/5.2/topics/db/examples/one_to_one/

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Owner {self.user.username}"

class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Reviewer {self.user.username}"