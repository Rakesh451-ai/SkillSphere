from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skillsphere.api_views import (
    SkillViewSet, StudyLogViewSet, GoalViewSet,
    RecommendationViewSet, UserProfileView,
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='api-skills')
router.register(r'studylogs', StudyLogViewSet, basename='api-studylogs')
router.register(r'goals', GoalViewSet, basename='api-goals')
router.register(r'recommendations', RecommendationViewSet, basename='api-recommendations')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileView.as_view(), name='api-profile'),
]
