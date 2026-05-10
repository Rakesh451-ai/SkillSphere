from django.db import models
from django.conf import settings


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume_analyses')
    resume_file = models.FileField(upload_to='resumes/')
    score = models.PositiveIntegerField(default=0, help_text='Resume score 0-100')
    suggestions = models.JSONField(default=list)
    skills_found = models.JSONField(default=list)
    sections_found = models.JSONField(default=list)
    missing_sections = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Resume Analyses'

    def __str__(self):
        return f"{self.user.username} - Resume ({self.score}/100)"
