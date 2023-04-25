from django.contrib import admin

from .models import Item, User, Bid, Category

# Register your models here.
admin.site.register([Item, User, Bid, Category])
