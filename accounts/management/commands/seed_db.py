import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from accounts.models import User

class Command(BaseCommand):
    help = 'Seeds initial database data from seed_data.json if database is empty'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force loading seed data even if users exist',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        user_count = User.objects.count()

        if user_count == 0 or force:
            self.stdout.write(self.style.SUCCESS("Loading seed data from seed_data.json..."))
            try:
                call_command('loaddata', 'seed_data.json')
                self.stdout.write(self.style.SUCCESS(f"Successfully loaded seed data! Total users: {User.objects.count()}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error loading seed data: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Database already contains {user_count} user(s). Skipping seed data loading."))
