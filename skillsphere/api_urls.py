from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skillsphere.api_views import (
    RecommendationViewSet, UserProfileView,
)

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet, basename='api-recommendations')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileView.as_view(), name='api-profile'),
]
