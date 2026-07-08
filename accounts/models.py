from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    college = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    skills_list = models.TextField(blank=True, help_text='Comma-separated list of skills')
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    xp_points = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    game_typer_level = models.PositiveIntegerField(default=0)
    game_bug_level = models.PositiveIntegerField(default=0)
    game_complexity_level = models.PositiveIntegerField(default=0)
    game_parsons_level = models.PositiveIntegerField(default=0)
    game_predictor_level = models.PositiveIntegerField(default=0)
    leetcode_username = models.CharField(max_length=100, blank=True)
    leetcode_easy_solved = models.PositiveIntegerField(default=0)
    leetcode_medium_solved = models.PositiveIntegerField(default=0)
    leetcode_hard_solved = models.PositiveIntegerField(default=0)
    leetcode_last_sync = models.DateTimeField(null=True, blank=True)
    leetcode_last_penalty_date = models.DateField(null=True, blank=True)
    completed_dsa_problems = models.JSONField(default=list)

    def __str__(self):
        return self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def leetcode_total_solved(self):
        return self.leetcode_easy_solved + self.leetcode_medium_solved + self.leetcode_hard_solved

    @property
    def leetcode_rank(self):
        if not self.leetcode_username:
            return None
        from django.db.models import F
        total_solved = self.leetcode_total_solved
        better_users = User.objects.filter(is_active=True, is_staff=False).annotate(
            tot=F('leetcode_easy_solved') + F('leetcode_medium_solved') + F('leetcode_hard_solved')
        ).filter(tot__gt=total_solved).count()
        return better_users + 1
