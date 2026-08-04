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

    if sort_by == 'streak':
        users = users.order_by('-current_streak')
    elif sort_by == 'leetcode':
        from django.db.models import F
        users = users.annotate(
            total_leetcode=F('leetcode_easy_solved') + F('leetcode_medium_solved') + F('leetcode_hard_solved')
        ).order_by('-total_leetcode')
    else:
        users = users.order_by('-xp_points')

    # Add rank numbers
    ranked_users = []
    for i, user in enumerate(users[:50], 1):
        ranked_users.append({
            'rank': i,
            'user': user,
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
