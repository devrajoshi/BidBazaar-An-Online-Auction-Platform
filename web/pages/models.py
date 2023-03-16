from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings
import urllib.request

@deconstructible
class AbsoluteUrlStorage(Storage):
    def __init__(self, location=None, base_url=None):
        self.base_url = base_url or settings.MEDIA_URL
        self.location = location or settings.MEDIA_ROOT

    def _open(self, name, mode='rb'):
        return urllib.request.urlopen(name)

    def _save(self, name, content):
        # Here you can define your own logic for storing the file, 
        # such as uploading it to a remote server via HTTP.
        return name

    def url(self, name):
        return name

class User(models.Model):
    user = models.OneToOneField(
        DjangoUser, on_delete=models.CASCADE, related_name="profile"
    )
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    pan_no = models.PositiveIntegerField(blank=True, null=True)
    citizen_no = models.PositiveIntegerField(blank=True, null=True)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_full_name()

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(storage=AbsoluteUrlStorage(), blank=True)
    price = models.BigIntegerField()
    seller = models.ForeignKey(DjangoUser, on_delete=models.PROTECT)
    added_at = models.DateTimeField(auto_now_add=True)
    deadline_at = models.DateTimeField(blank=True)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    bid_at = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(DjangoUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.item
