import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

for user in User.objects.all():
    try:
        user.profile
        print(f'Profile exists for {user.username}')
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)
        print(f'Created profile for {user.username}')
