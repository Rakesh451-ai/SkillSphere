import json
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count
from django.shortcuts import render
from django.utils import timezone

from goals.models import Goal
from skills.models import Skill
from studylogs.models import StudyLog
from recommendations.models import Recommendation


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


@login_required
def home(request):
    user = request.user
    now = timezone.now()
    today = now.date()

    # Study stats
    all_logs = StudyLog.objects.filter(user=user)
    total_hours = all_logs.aggregate(total=Sum('hours'))['total'] or 0

    # Weekly data (last 7 days)
    weekly_data = []
    weekly_labels = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_hours = all_logs.filter(date=day).aggregate(total=Sum('hours'))['total'] or 0
        weekly_data.append(float(day_hours))
        weekly_labels.append(day.strftime('%a'))

    # Skill data
    skills = Skill.objects.filter(user=user)
    skill_names = [s.skill_name[:15] for s in skills[:8]]
    skill_hours = [float(s.hours_practiced) for s in skills[:8]]

    # Goals stats
    goals = Goal.objects.filter(user=user)
    completed_goals = goals.filter(status='completed').count()
    total_goals = goals.count()

    # Productivity data (last 7 days)
    productivity_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        avg_prod = all_logs.filter(date=day).aggregate(avg=Avg('productivity'))['avg'] or 0
        productivity_data.append(round(float(avg_prod), 1))

    # Monthly analytics (last 4 weeks)
    monthly_labels = []
    monthly_hours = []
    for i in range(3, -1, -1):
        week_start = today - timedelta(weeks=i + 1)
        week_end = today - timedelta(weeks=i)
        hours = all_logs.filter(date__gte=week_start, date__lt=week_end).aggregate(
            total=Sum('hours'))['total'] or 0
        monthly_labels.append(f'Week {4 - i}')
        monthly_hours.append(float(hours))

    # Placement readiness
    placement_score = calculate_placement_readiness(user)

    # Productivity score
    recent_logs = all_logs.filter(date__gte=today - timedelta(days=7))
    productivity_score = recent_logs.aggregate(avg=Avg('productivity'))['avg'] or 0
    productivity_score = round(float(productivity_score) * 10, 1)

    # Most improved and weakest skills
    most_improved = skills.order_by('-hours_practiced').first()
    weakest = skills.order_by('hours_practiced').first()

    # Recent recommendations
    recommendations = Recommendation.objects.filter(user=user)[:3]

    context = {
        'total_hours': float(total_hours),
        'current_streak': user.current_streak,
        'placement_score': placement_score,
        'completed_goals': completed_goals,
        'total_goals': total_goals,
        'productivity_score': productivity_score,
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_data': json.dumps(weekly_data),
        'skill_names': json.dumps(skill_names),
        'skill_hours': json.dumps(skill_hours),
        'productivity_data': json.dumps(productivity_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_hours': json.dumps(monthly_hours),
        'most_improved': most_improved,
        'weakest': weakest,
        'recommendations': recommendations,
        'xp_points': user.xp_points,
    }
    return render(request, 'dashboard/home.html', context)


def calculate_placement_readiness(user):
    score = 0
    max_score = 100

    # Skill levels (30 points)
    skills = Skill.objects.filter(user=user)
    if skills.exists():
        advanced = skills.filter(level='advanced').count()
        intermediate = skills.filter(level='intermediate').count()
        skill_score = min((advanced * 10 + intermediate * 5), 30)
        score += skill_score

    # Study consistency (20 points)
    if user.current_streak >= 14:
        score += 20
    elif user.current_streak >= 7:
        score += 15
    elif user.current_streak >= 3:
        score += 10
    elif user.current_streak >= 1:
        score += 5

    # Goal completion (20 points)
    goals = Goal.objects.filter(user=user)
    if goals.exists():
        completed = goals.filter(status='completed').count()
        total = goals.count()
        score += int((completed / total) * 20)

    # Resume quality (15 points)
    from resumeanalyzer.models import ResumeAnalysis
    latest_resume = ResumeAnalysis.objects.filter(user=user).first()
    if latest_resume:
        score += int(latest_resume.score * 0.15)

    # Study hours (15 points)
    total_hours = StudyLog.objects.filter(user=user).aggregate(
        total=Sum('hours'))['total'] or 0
    if total_hours >= 200:
        score += 15
    elif total_hours >= 100:
        score += 10
    elif total_hours >= 50:
        score += 7
    elif total_hours >= 20:
        score += 4

    return min(score, max_score)


@login_required
def analytics(request):
    user = request.user
    today = timezone.now().date()
    all_logs = StudyLog.objects.filter(user=user)

    # Category distribution
    category_data = {}
    for log in all_logs:
        cat = log.get_category_display()
        category_data[cat] = category_data.get(cat, 0) + float(log.hours)

    # Daily heatmap data (last 30 days)
    heatmap_data = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        hours = all_logs.filter(date=day).aggregate(total=Sum('hours'))['total'] or 0
        heatmap_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day.strftime('%a'),
            'hours': float(hours),
        })

    # Goal completion rate by type
    goals = Goal.objects.filter(user=user)
    goal_stats = {}
    for goal_type, label in Goal.TYPE_CHOICES:
        type_goals = goals.filter(goal_type=goal_type)
        total = type_goals.count()
        completed = type_goals.filter(status='completed').count()
        goal_stats[label] = {
            'total': total,
            'completed': completed,
            'rate': round(completed / total * 100) if total > 0 else 0,
        }

    context = {
        'category_labels': json.dumps(list(category_data.keys())),
        'category_data': json.dumps(list(category_data.values())),
        'heatmap_data': json.dumps(heatmap_data),
        'goal_stats': goal_stats,
    }
    return render(request, 'dashboard/analytics.html', context)
