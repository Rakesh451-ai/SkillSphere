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

# 2. Promote all admin user accounts (admin, Ayush, Test, admin_user, etc.)
default_admin_list = ['admin', 'admin_user', 'Ayush', 'Test', 'rakesh', 'Rakesh']
env_admins = [a.strip() for a in os.environ.get('ADMIN_USERNAMES', '').split(',') if a.strip()]
target_admins = set(default_admin_list + env_admins)

for admin_name in target_admins:
    u = User.objects.filter(username__iexact=admin_name).first()
    if u:
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print(f"User '{u.username}' promoted to Admin / Superuser successfully!")

# 3. If environment flag PROMOTE_ALL_USERS=True is set, promote all active users
if os.environ.get('PROMOTE_ALL_USERS', 'True').lower() in ('true', '1', 'yes'):
    for user_obj in User.objects.all():
        if not user_obj.is_staff or not user_obj.is_superuser:
            user_obj.is_staff = True
            user_obj.is_superuser = True
            user_obj.save()
            print(f"Auto-promoted user '{user_obj.username}' to Admin / Superuser!")

