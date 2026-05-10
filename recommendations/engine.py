"""Rule-based AI recommendation engine for student growth analysis."""

from datetime import timedelta
from decimal import Decimal

from django.db.models import Avg, Sum
from django.utils import timezone


def generate_recommendations(user):
    """Analyze user activity and generate smart recommendations."""
    from studylogs.models import StudyLog
    from skills.models import Skill
    from goals.models import Goal
    from .models import Recommendation

    recommendations = []
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    recent_logs = StudyLog.objects.filter(user=user, date__gte=week_ago.date())
    older_logs = StudyLog.objects.filter(user=user, date__gte=two_weeks_ago.date(), date__lt=week_ago.date())

    recent_hours = recent_logs.aggregate(total=Sum('hours'))['total'] or Decimal('0')
    older_hours = older_logs.aggregate(total=Sum('hours'))['total'] or Decimal('0')

    recent_avg_prod = recent_logs.aggregate(avg=Avg('productivity'))['avg'] or 0

    # Check study consistency
    if recent_hours < older_hours and older_hours > 0:
        drop_pct = round((1 - float(recent_hours) / float(older_hours)) * 100)
        recommendations.append({
            'message': f'Your study hours dropped by {drop_pct}% this week. Try to maintain consistency.',
            'category': 'Consistency',
            'priority': 'high' if drop_pct > 50 else 'medium',
        })

    # Check productivity
    if recent_avg_prod and recent_avg_prod < 5:
        recommendations.append({
            'message': 'Your average productivity is below 5/10. Consider better study planning and reducing distractions.',
            'category': 'Productivity',
            'priority': 'high',
        })
    elif recent_avg_prod and recent_avg_prod < 7:
        recommendations.append({
            'message': 'Your productivity could improve. Try the Pomodoro technique or study in focused blocks.',
            'category': 'Productivity',
            'priority': 'medium',
        })

    # Check skill-specific practice
    skills = Skill.objects.filter(user=user)
    for skill in skills:
        if skill.category == 'DSA' and skill.hours_practiced < 20:
            recommendations.append({
                'message': f'Practice more DSA ({skill.skill_name}). Consistent practice is key for placements.',
                'category': 'DSA',
                'priority': 'high',
            })
        if skill.category == 'COMM' and skill.level == 'beginner':
            recommendations.append({
                'message': 'Improve communication skills. Practice speaking and join group discussions.',
                'category': 'Communication',
                'priority': 'medium',
            })

    # Check goals completion
    total_goals = Goal.objects.filter(user=user).count()
    completed_goals = Goal.objects.filter(user=user, status='completed').count()
    if total_goals > 0:
        completion_rate = completed_goals / total_goals * 100
        if completion_rate < 30:
            recommendations.append({
                'message': f'Only {completion_rate:.0f}% of your goals are completed. Break larger goals into smaller tasks.',
                'category': 'Goals',
                'priority': 'high',
            })

    # No recent activity
    if not recent_logs.exists():
        recommendations.append({
            'message': 'No study activity logged this week. Start small — even 30 minutes daily makes a difference.',
            'category': 'Consistency',
            'priority': 'high',
        })

    # General encouragement
    if recent_hours >= 15:
        recommendations.append({
            'message': 'Great work this week! Keep up the momentum. Consider challenging yourself with harder topics.',
            'category': 'Motivation',
            'priority': 'low',
        })

    # Check category balance
    category_hours = {}
    for log in recent_logs:
        category_hours[log.category] = category_hours.get(log.category, Decimal('0')) + log.hours

    if category_hours and len(category_hours) < 3:
        recommendations.append({
            'message': 'Diversify your study topics. Well-rounded preparation improves placement readiness.',
            'category': 'Balance',
            'priority': 'medium',
        })

    # Save recommendations
    Recommendation.objects.filter(user=user).delete()
    for rec in recommendations:
        Recommendation.objects.create(user=user, **rec)

    return recommendations
