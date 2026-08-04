from django.db import models
from django.conf import settings


class Recommendation(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=255, blank=True, default='')
    message = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    action_text = models.CharField(max_length=100, blank=True, default='')
    action_url = models.CharField(max_length=255, blank=True, default='')
    icon = models.CharField(max_length=50, default='bi-lightbulb-fill')
    impact_badge = models.CharField(max_length=50, blank=True, default='')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title or self.message[:50]}"
