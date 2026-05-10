from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class StudyLog(models.Model):
    CATEGORY_CHOICES = [
        ('DSA', 'Data Structures & Algorithms'),
        ('WEBDEV', 'Web Development'),
        ('COMM', 'Communication'),
        ('APT', 'Aptitude'),
        ('AIML', 'AI/ML'),
        ('CORE', 'Core Subjects'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_logs')
    topic = models.CharField(max_length=200)
    hours = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0.1)])
    productivity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Rate 1-10',
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    notes = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.topic} ({self.date})"
