from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seller = models.CharField(max_length=255)
    seller_id = models.PositiveBigIntegerField(default=0)
    image = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    deadline_at = models.DateTimeField(blank=True)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    
    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return self.get_full_name()
