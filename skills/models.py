from django.db import models
from django.conf import settings


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('DSA', 'Data Structures & Algorithms'),
        ('WEBDEV', 'Web Development'),
        ('COMM', 'Communication'),
        ('APT', 'Aptitude'),
        ('AIML', 'AI/ML'),
        ('CORE', 'Core Subjects'),
        ('OTHER', 'Other'),
    ]
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    hours_practiced = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    progress = models.PositiveIntegerField(default=0, help_text='Progress percentage 0-100')
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'skill_name']
        ordering = ['-hours_practiced']

    def __str__(self):
        return f"{self.user.username} - {self.skill_name} ({self.level})"

    def update_level(self):
        if self.hours_practiced >= 100:
            self.level = 'advanced'
        elif self.hours_practiced >= 30:
            self.level = 'intermediate'
        else:
            self.level = 'beginner'
