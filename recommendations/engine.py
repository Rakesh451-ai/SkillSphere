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
    from resumeanalyzer.models import ResumeAnalysis
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

    # 1. Check study consistency (Existing Rule)
    if recent_hours < older_hours and older_hours > 0:
        drop_pct = round((1 - float(recent_hours) / float(older_hours)) * 100)
        recommendations.append({
            'message': f'Your study hours dropped by {drop_pct}% this week. Try to maintain consistency.',
            'category': 'Consistency',
            'priority': 'high' if drop_pct > 50 else 'medium',
        })

    # 2. Check productivity (Existing Rule + Peak Productivity)
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
    elif recent_avg_prod >= 8:
        recommendations.append({
            'message': f'Excellent productivity! You averaged {recent_avg_prod:.1f}/10 this week. Keep up the great habits.',
            'category': 'Productivity',
            'priority': 'low',
        })

    # 3. Check skill-specific practice (Existing Rules + Enhancements)
    skills = Skill.objects.filter(user=user)
    if not skills.exists():
        recommendations.append({
            'message': 'You have not added any skills to track. Go to the Skills section to add your target skills.',
            'category': 'Skills',
            'priority': 'medium',
        })
    else:
        for skill in skills:
            if skill.category == 'DSA' and skill.hours_practiced < 20:
                recommendations.append({
                    'message': f'Practice more DSA ({skill.skill_name}). Consistent practice is key for placements.',
                    'category': 'DSA',
                    'priority': 'high',
                })
            elif skill.category == 'COMM' and skill.level == 'beginner':
                recommendations.append({
                    'message': 'Improve communication skills. Practice speaking and join group discussions.',
                    'category': 'Communication',
                    'priority': 'medium',
                })
            elif skill.level == 'beginner':
                if skill.category == 'WEBDEV':
                    recommendations.append({
                        'message': f'As a beginner in Web Development ({skill.skill_name}), try building a small project (like a portfolio) to apply your knowledge.',
                        'category': 'Web Dev',
                        'priority': 'medium',
                    })
                elif skill.category == 'AIML':
                    recommendations.append({
                        'message': f'You are starting with AI/ML ({skill.skill_name}). Focus on core math/statistics and Python basics first.',
                        'category': 'AI/ML',
                        'priority': 'medium',
                    })
                elif skill.category == 'APT':
                    recommendations.append({
                        'message': f'Aptitude is crucial for early placement tests. Practice problems for {skill.skill_name} daily.',
                        'category': 'Aptitude',
                        'priority': 'medium',
                    })
            elif skill.level == 'intermediate' and 70 <= skill.hours_practiced < 100:
                hours_left = 100 - float(skill.hours_practiced)
                recommendations.append({
                    'message': f'You are close to advanced level in {skill.skill_name}! Practice {hours_left:.1f} more hours to upgrade your level.',
                    'category': skill.get_category_display(),
                    'priority': 'medium',
                })

    # 4. Check goals completion (Existing Rules + Upcoming Deadlines)
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
        elif completion_rate >= 70 and total_goals >= 3:
            recommendations.append({
                'message': f'Incredible job! You have completed {completion_rate:.0f}% of your goals. Keep striving for excellence!',
                'category': 'Goals',
                'priority': 'low',
            })

    # Check upcoming goal deadlines (next 2 days)
    today_date = timezone.localdate()
    two_days_later = today_date + timedelta(days=2)
    upcoming_goals = Goal.objects.filter(
        user=user,
        status__in=['pending', 'in_progress'],
        deadline__gte=today_date,
        deadline__lte=two_days_later
    )
    for goal in upcoming_goals[:2]:
        recommendations.append({
            'message': f'Upcoming deadline: "{goal.title}" is due on {goal.deadline}. Try to complete it!',
            'category': 'Goals',
            'priority': 'high',
        })

    # 5. Study streaks & Consistency motivation
    if user.current_streak >= 3:
        recommendations.append({
            'message': f'Awesome consistency! You are on a {user.current_streak}-day study streak. Keep it going!',
            'category': 'Consistency',
            'priority': 'low',
        })
    elif user.current_streak == 0 and user.longest_streak >= 5:
        recommendations.append({
            'message': f'Let\'s build your streak back up! Your record is a {user.longest_streak}-day streak. Log study logs to restart it.',
            'category': 'Consistency',
            'priority': 'medium',
        })

    # No recent activity
    if not recent_logs.exists():
        if not StudyLog.objects.filter(user=user).exists():
            recommendations.append({
                'message': 'Welcome to SkillSphere! Start your learning journey by logging your first study session to get personalized AI insights.',
                'category': 'Consistency',
                'priority': 'high',
            })
        else:
            recommendations.append({
                'message': 'No study activity logged this week. Start small — even 30 minutes daily makes a difference.',
                'category': 'Consistency',
                'priority': 'high',
            })

    # General encouragement & Burnout warning
    if recent_hours >= 35:
        recommendations.append({
            'message': f'You logged {recent_hours:.1f} hours of study this week. Outstanding work, but make sure to take breaks and prevent burnout.',
            'category': 'Productivity',
            'priority': 'low',
        })
    elif recent_hours >= 15:
        recommendations.append({
            'message': 'Great work this week! Keep up the momentum. Consider challenging yourself with harder topics.',
            'category': 'Motivation',
            'priority': 'low',
        })

    # Check category balance (Existing Rule)
    category_hours = {}
    for log in recent_logs:
        category_hours[log.category] = category_hours.get(log.category, Decimal('0')) + log.hours

    if category_hours and len(category_hours) < 3:
        recommendations.append({
            'message': 'Diversify your study topics. Well-rounded preparation improves placement readiness.',
            'category': 'Balance',
            'priority': 'medium',
        })

    # 6. Resume Analysis Integration (New Enhancement)
    try:
        latest_resume = ResumeAnalysis.objects.filter(user=user).order_by('-created_at').first()
        if not latest_resume:
            recommendations.append({
                'message': 'You haven\'t analyzed your resume yet. Upload it in the Resume Analyzer to get score feedback and suggestions.',
                'category': 'Resume',
                'priority': 'medium',
            })
        else:
            if latest_resume.score < 60:
                recommendations.append({
                    'message': f'Your resume score is low ({latest_resume.score}/100). Check the Resume Analyzer for key suggestions to improve it.',
                    'category': 'Resume',
                    'priority': 'high',
                })
            
            missing_sections = latest_resume.missing_sections
            if missing_sections:
                sections_str = ", ".join(missing_sections[:2])
                recommendations.append({
                    'message': f'Your resume is missing important sections: {sections_str}. Add them to highlight your background.',
                    'category': 'Resume',
                    'priority': 'medium',
                })
    except Exception:
        # Gracefully ignore any database issues with resumeanalyzer
        pass

    # Save recommendations
    Recommendation.objects.filter(user=user).delete()
    for rec in recommendations:
        Recommendation.objects.create(user=user, **rec)

    return recommendations

