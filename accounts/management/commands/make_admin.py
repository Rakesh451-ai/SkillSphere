from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Promotes a user account to Superuser / Staff Admin status'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the account to promote to admin')

    def handle(self, *args, **options):
        username = options['username'].strip()
        user = User.objects.filter(username__iexact=username).first()

        if not user:
            self.stdout.write(self.style.ERROR(f"User with username '{username}' was not found."))
            return

        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully promoted user '{user.username}' (ID: {user.id}) to Admin / Superuser!"))
