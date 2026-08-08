from django.db import models
from django.conf import settings
from django.utils import timezone


class GameHistory(models.Model):
    GAME_CHOICES = [
        ('typer', 'Speed Typer'),
        ('bug', 'Bug Hunter'),
        ('complexity', 'Big-O Complexity Master'),
        ('parsons', 'Code Repair Shop'),
        ('predictor', 'Output Predictor'),
        ('algo', 'Algorithm Sequence Master'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_histories'
    )
    game_type = models.CharField(max_length=20, choices=GAME_CHOICES)
    level = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']
        verbose_name_plural = 'Game Histories'

    def __str__(self):
        return f"{self.user.username} - {self.get_game_type_display()} Level {self.level} ({self.score} XP)"

    @property
    def game_display_name(self):
        return dict(self.GAME_CHOICES).get(self.game_type, self.game_type)


class DiscussionPost(models.Model):
    POST_TYPES = [
        ('problem', 'Problem & Solution'),
        ('question', 'Question / Doubt'),
        ('chat', 'General Chat'),
        ('announcement', 'Admin Announcement'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discussion_posts'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Problem description or discussion text")
    code_snippet = models.TextField(blank=True, null=True, help_text="Optional problem/solution code snippet")
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='problem')
    category = models.CharField(max_length=50, default='General', help_text="e.g. C++, Python, DSA, Web Dev, Aptitude")
    upvotes = models.PositiveIntegerField(default=0)
    upvoted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='upvoted_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title} by @{self.user.username}"


class DiscussionReply(models.Model):
    post = models.ForeignKey(
        DiscussionPost,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discussion_replies'
    )
    content = models.TextField(help_text="Solution or reply content")
    code_solution = models.TextField(blank=True, null=True, help_text="Optional solution code snippet")
    is_solution = models.BooleanField(default=False, help_text="Mark as verified solution")
    upvotes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by @{self.user.username} on '{self.post.title}'"


class ChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    message = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Chat message from @{self.user.username} at {self.created_at}"


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100, default='General DSA', help_text="DSA Topic e.g. Array, String, Heap, DP")
    difficulty = models.CharField(max_length=50, default='Basic to Advanced', help_text="Difficulty level e.g. Basic to Advanced")
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(help_text="Quiz start date and time")
    end_time = models.DateTimeField(help_text="Quiz end date and time")
    is_live = models.BooleanField(default=True, help_text="Is quiz published?")
    total_xp = models.PositiveIntegerField(default=100, help_text="XP awarded for completion")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f"{self.title} ({self.status_display})"

    @property
    def status(self):
        now = timezone.now()
        if not self.is_live:
            return 'draft'
        if now < self.start_time:
            return 'upcoming'
        elif self.start_time <= now <= self.end_time:
            return 'live'
        else:
            return 'ended'

    @property
    def status_display(self):
        s = self.status
        if s == 'draft': return 'Draft'
        if s == 'upcoming': return 'Upcoming'
        if s == 'live': return 'Live Now'
        return 'Ended'


class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ('single', 'Single Choice (Radio)'),
        ('multiple', 'Multiple Choice (Checkboxes)'),
        ('text', 'Text Answer'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='single')
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.TextField(help_text="e.g. A or A,B or text answer")
    explanation = models.TextField(blank=True, null=True)
    points = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"Q: {self.question_text[:40]} ({self.get_question_type_display()})"


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_submissions')
    score = models.IntegerField(default=0)
    total_possible = models.IntegerField(default=0)
    xp_awarded = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user')
        ordering = ['-score', 'submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.score}/{self.total_possible}"
