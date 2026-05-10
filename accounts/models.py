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

    def __str__(self):
        return self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.username
