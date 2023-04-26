import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User

# Enter the desired username and password
username = "admin"
password = "admin"

# Create the superuser
superuser = User.objects.create_superuser(username=username, password=password)
print(f"Superuser {superuser.username} created!")
