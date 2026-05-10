from rest_framework import viewsets, generics, serializers
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from skills.models import Skill
from studylogs.models import StudyLog
from goals.models import Goal
from recommendations.models import Recommendation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'college', 'branch', 'year', 'bio', 'xp_points',
            'current_streak', 'longest_streak',
        ]
        read_only_fields = ['id', 'username', 'xp_points', 'current_streak', 'longest_streak']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name', 'category', 'hours_practiced', 'level', 'progress', 'last_updated']
        read_only_fields = ['id', 'last_updated']


class StudyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyLog
        fields = ['id', 'topic', 'hours', 'productivity', 'category', 'notes', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'goal_type', 'status', 'progress', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'message', 'category', 'priority', 'is_read', 'created_at']
        read_only_fields = ['id', 'message', 'category', 'priority', 'created_at']


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudyLogViewSet(viewsets.ModelViewSet):
    serializer_class = StudyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
