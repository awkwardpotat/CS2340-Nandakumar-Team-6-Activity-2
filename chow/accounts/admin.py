from django.contrib import admin
from .models import Owner, Reviewer

# Register your models here.
admin.site.register(Owner)
admin.site.register(Reviewer)