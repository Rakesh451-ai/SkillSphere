import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from accounts.models import User

# Read from environment variables or use safe defaults
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'smbi@123')

# 1. Create or update main default superuser
user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()
print(f"Superuser '{username}' configured successfully!")

# 2. Promote any additional usernames passed in ADMIN_USERNAMES environment variable (e.g. "rakesh,john")
additional_admins = os.environ.get('ADMIN_USERNAMES', '').split(',')
for admin_name in additional_admins:
    admin_name = admin_name.strip()
    if admin_name:
        u = User.objects.filter(username__iexact=admin_name).first()
        if u:
            u.is_staff = True
            u.is_superuser = True
            u.save()
            print(f"User '{u.username}' promoted to Admin / Superuser successfully!")

