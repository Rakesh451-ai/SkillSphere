from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F

from accounts.models import User
from .models import Badge, UserBadge


DEFAULT_BADGES = [
    {
        'name': 'Bronze Solver',
        'questions_required': 50,
        'tier': 'Bronze',
        'icon': 'fa-award',
        'description': 'Solved 50 problem-solving challenges! You have taken your first major step into algorithm mastery.'
    },
    {
        'name': 'Silver Centurion',
        'questions_required': 100,
        'tier': 'Silver',
        'icon': 'fa-medal',
        'description': 'Reached the 100 solved questions milestone! Your problem-solving speed and accuracy are building up.'
    },
    {
        'name': 'Gold Master',
        'questions_required': 150,
        'tier': 'Gold',
        'icon': 'fa-trophy',
        'description': 'Conquered 150 DSA problems! You are now well-prepared for technical interview rounds.'
    },
    {
        'name': 'Platinum Legend',
        'questions_required': 250,
        'tier': 'Platinum',
        'icon': 'fa-gem',
        'description': 'Crushed 250 coding challenges! You have mastered core data structures, algorithms, and paradigms.'
    },
    {
        'name': 'Diamond Overlord',
        'questions_required': 500,
        'tier': 'Diamond',
        'icon': 'fa-crown',
        'description': 'Elite milestone of 500 solved questions! Top 1% problem solver with impressive technical depth.'
    },
    {
        'name': 'Grandmaster Titan',
        'questions_required': 1000,
        'tier': 'Master',
        'icon': 'fa-dragon',
        'description': 'Legendary achievement of 1000 solved problems! Absolute grandmaster level in competitive programming and DSA.'
    },
]


def ensure_default_badges():
    for data in DEFAULT_BADGES:
        Badge.objects.get_or_create(
            name=data['name'],
            defaults={
                'questions_required': data['questions_required'],
                'tier': data['tier'],
                'icon': data['icon'],
                'description': data['description'],
            }
        )


def check_and_grant_badges(user):
    ensure_default_badges()
    completed_dsa = len(user.completed_dsa_problems) if isinstance(user.completed_dsa_problems, list) else 0
    total_solved = completed_dsa + user.leetcode_total_solved

    all_badges = Badge.objects.all().order_by('questions_required')
    user_badge_ids = set(UserBadge.objects.filter(user=user).values_list('badge_id', flat=True))

    for badge in all_badges:
        if badge.questions_required > 0 and total_solved >= badge.questions_required:
            if badge.id not in user_badge_ids:
                UserBadge.objects.create(user=user, badge=badge)


@login_required
def leaderboard_view(request):
    sort_by = request.GET.get('sort', 'leetcode')

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

    check_and_grant_badges(user)

    users = User.objects.filter(is_active=True, is_staff=False)
    users = users.annotate(
        total_leetcode=F('leetcode_easy_solved') + F('leetcode_medium_solved') + F('leetcode_hard_solved')
    )
    if sort_by == 'streak':
        users = users.order_by('-current_streak', '-longest_streak', 'username')
    elif sort_by == 'xp':
        users = users.order_by('-xp_points', 'username')
    else:
        users = users.order_by('-total_leetcode', 'username')

    ranked_users = []
    for i, u in enumerate(users[:50], 1):
        ranked_users.append({
            'rank': i,
            'user': u,
        })

    return render(request, 'leaderboard/leaderboard.html', {
        'ranked_users': ranked_users,
        'sort_by': sort_by,
    })


@login_required
def badges_view(request):
    check_and_grant_badges(request.user)

    all_badges = Badge.objects.all().order_by('questions_required')
    user_badges_map = {ub.badge_id: ub.earned_at for ub in UserBadge.objects.filter(user=request.user)}

    completed_dsa = len(request.user.completed_dsa_problems) if isinstance(request.user.completed_dsa_problems, list) else 0
    total_solved = completed_dsa + request.user.leetcode_total_solved

    badges_data = []
    next_badge = None
    next_badge_remaining = 0
    next_badge_pct = 0

    for badge in all_badges:
        earned = badge.id in user_badges_map
        earned_at = user_badges_map.get(badge.id)

        req = badge.questions_required
        if req > 0:
            pct = min(100, round((total_solved / req) * 100))
            remaining = max(0, req - total_solved)
        else:
            pct = 100
            remaining = 0

        if not earned and next_badge is None and req > 0:
            next_badge = badge
            next_badge_remaining = remaining
            next_badge_pct = pct

        badges_data.append({
            'badge': badge,
            'earned': earned,
            'earned_at': earned_at,
            'progress_pct': pct,
            'remaining_qs': remaining,
        })

    unlocked_count = sum(1 for b in badges_data if b['earned'])

    return render(request, 'leaderboard/badges.html', {
        'badges_data': badges_data,
        'total_solved': total_solved,
        'unlocked_count': unlocked_count,
        'total_badges': len(badges_data),
        'next_badge': next_badge,
        'next_badge_remaining': next_badge_remaining,
        'next_badge_pct': next_badge_pct,
    })
