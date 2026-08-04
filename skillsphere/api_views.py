from rest_framework import viewsets, generics, serializers
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
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


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'message', 'category', 'priority', 'is_read', 'created_at']
        read_only_fields = ['id', 'message', 'category', 'priority', 'created_at']


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
