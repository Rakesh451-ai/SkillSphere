from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from accounts.models import User
from .models import Badge, UserBadge


@login_required
def leaderboard_view(request):
    sort_by = request.GET.get('sort', 'xp')

    # Trigger LeetCode sync for current user if applicable
    user = request.user
    if user.leetcode_username:
        from django.utils import timezone
        now = timezone.now()
        if not user.leetcode_last_sync or now - user.leetcode_last_sync > timezone.timedelta(minutes=10):
            try:
                from accounts.leetcode import sync_leetcode_stats
                sync_leetcode_stats(user)
            except Exception:
                pass

    users = User.objects.filter(is_active=True, is_staff=False)

    from django.db.models import F
    users = users.annotate(
        total_leetcode=F('leetcode_easy_solved') + F('leetcode_medium_solved') + F('leetcode_hard_solved')
    )

    if sort_by == 'streak':
        users = users.order_by('-current_streak', '-total_leetcode', '-xp_points')
    elif sort_by == 'leetcode':
        users = users.order_by('-total_leetcode', '-current_streak', '-xp_points')
    elif sort_by == 'hours':
        users = users.order_by('-total_leetcode', '-xp_points', '-current_streak')
    else:
        users = users.order_by('-xp_points', '-current_streak', '-total_leetcode')

    # Add rank numbers & calculated activity stats
    ranked_users = []
    for i, u in enumerate(users[:50], 1):
        completed_dsa = len(u.completed_dsa_problems) if isinstance(u.completed_dsa_problems, list) else 0
        game_levels = u.game_typer_level + u.game_bug_level + u.game_complexity_level + u.game_parsons_level + u.game_predictor_level
        total_hours = round((completed_dsa * 0.5) + (u.leetcode_total_solved * 0.4) + (game_levels * 0.2), 1)

        ranked_users.append({
            'rank': i,
            'user': u,
            'completed_goals': completed_dsa,
            'total_hours': total_hours,
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
