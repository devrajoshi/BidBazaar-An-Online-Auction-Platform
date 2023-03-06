from django.contrib import admin

from .models import Item, User, Bid

# Register your models here.
admin.site.register([Item, User, Bid])
