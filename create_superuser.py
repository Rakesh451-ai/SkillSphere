import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from accounts.models import User

# Read from environment variables or use safe defaults
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'smbi@123')

user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()

if created:
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' updated with specified password successfully!")
