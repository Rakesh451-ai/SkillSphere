from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Recommendation
from .engine import generate_recommendations


@login_required
def recommendation_list(request):
    if request.GET.get('refresh') == '1':
        generate_recommendations(request.user)
    recommendations = Recommendation.objects.filter(user=request.user)
    if not recommendations.exists():
        generate_recommendations(request.user)
        recommendations = Recommendation.objects.filter(user=request.user)
    return render(request, 'recommendations/recommendation_list.html', {
        'recommendations': recommendations,
    })
