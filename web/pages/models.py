from django.db import models
from django.contrib.auth.models import User as DjangoUser

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
    image = models.ImageField(blank=True)
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
