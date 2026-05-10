from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from accounts.models import User
from studylogs.models import StudyLog
from goals.models import Goal
from .models import Badge, UserBadge


@login_required
def leaderboard_view(request):
    sort_by = request.GET.get('sort', 'xp')

    users = User.objects.filter(is_active=True, is_staff=False)

    if sort_by == 'hours':
        users = users.annotate(
            total_hours=Sum('study_logs__hours')
        ).order_by('-total_hours')
    elif sort_by == 'goals':
        users = users.annotate(
            completed_goals=Count('goals', filter=Goal.objects.filter(status='completed').query.where)
        ).order_by('-completed_goals') if False else users.order_by('-xp_points')
    elif sort_by == 'streak':
        users = users.order_by('-current_streak')
    else:
        users = users.order_by('-xp_points')

    # Add rank numbers
    ranked_users = []
    for i, user in enumerate(users[:50], 1):
        total_hours = StudyLog.objects.filter(user=user).aggregate(
            total=Sum('hours'))['total'] or 0
        completed_goals = Goal.objects.filter(user=user, status='completed').count()
        ranked_users.append({
            'rank': i,
            'user': user,
            'total_hours': total_hours,
            'completed_goals': completed_goals,
        })

    return render(request, 'leaderboard/leaderboard.html', {
        'ranked_users': ranked_users,
        'sort_by': sort_by,
    })


@login_required
def badges_view(request):
    all_badges = Badge.objects.all()
    user_badges = UserBadge.objects.filter(user=request.user).values_list('badge_id', flat=True)

    badges_data = []
    for badge in all_badges:
        badges_data.append({
            'badge': badge,
            'earned': badge.id in user_badges,
        })

    return render(request, 'leaderboard/badges.html', {'badges_data': badges_data})
