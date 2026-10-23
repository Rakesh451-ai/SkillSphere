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
        from dashboard.models import Quiz
        quiz_count = Quiz.objects.count()

        if user_count <= 1 or quiz_count == 0 or force:
            data_dir = os.path.join(os.getcwd(), 'data')
            data_files = []
            if os.path.exists(data_dir):
                data_files = sorted([
                    os.path.join('data', f)
                    for f in os.listdir(data_dir)
                    if f.endswith('.json')
                ])

            if data_files:
                self.stdout.write(self.style.SUCCESS(f"Loading seed data from {len(data_files)} fixture files in data/ ..."))
                try:
                    call_command('loaddata', *data_files)
                    self.stdout.write(self.style.SUCCESS(f"Successfully loaded seed data from data/! Users: {User.objects.count()}, Quizzes: {Quiz.objects.count()}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading seed data from data/: {e}"))
            elif os.path.exists('seed_data.json'):
                self.stdout.write(self.style.SUCCESS("Loading seed data from seed_data.json..."))
                try:
                    call_command('loaddata', 'seed_data.json')
                    self.stdout.write(self.style.SUCCESS(f"Successfully loaded seed data! Users: {User.objects.count()}, Quizzes: {Quiz.objects.count()}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading seed data: {e}"))
            else:
                self.stdout.write(self.style.WARNING("No seed fixtures found in data/ or seed_data.json."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Database contains {user_count} user(s) and {quiz_count} quiz(zes). Skipping seed data loading."))
