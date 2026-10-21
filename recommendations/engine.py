"""Enhanced AI recommendation engine for student growth, Big-O Master, and placement readiness analysis."""

from datetime import timedelta
from django.utils import timezone
from django.urls import reverse


def generate_recommendations(user):
    """Analyze user activity across placement score, DSA sheet, LeetCode, games, quizzes, and resume to generate targeted AI recommendations."""
    from resume_analysis.models import ResumeAnalysis
    from dashboard.models import Quiz, QuizSubmission, DiscussionPost, DiscussionReply
    from dashboard.views import DSA_SHEET, calculate_placement_readiness
    from .models import Recommendation

    recommendations = []
    completed_dsa = user.completed_dsa_problems or []

    games_url = reverse('dashboard:cpp_calculator')
    study_url = reverse('dashboard:study_materials')
    quiz_url = reverse('dashboard:quiz_list')
    leaderboard_url = reverse('leaderboard:leaderboard')
    resume_url = reverse('resume_analysis:upload')
    discussions_url = reverse('dashboard:discussions')
    home_url = reverse('dashboard:home')

    # 1. Placement Readiness Analysis
    placement_score = calculate_placement_readiness(user)
    if placement_score < 60:
        recommendations.append({
            'title': 'Accelerate Placement Readiness',
            'message': f'Your placement readiness is at {placement_score}%. Solve core DSA problems and complete arcade coding games to reach 80%+ target readiness.',
            'category': 'Placement Readiness',
            'priority': 'high',
            'action_text': 'Explore Prep Hub',
            'action_url': study_url,
            'icon': 'bi-briefcase-fill',
            'impact_badge': f'Current: {placement_score}%',
        })
    elif placement_score >= 85:
        recommendations.append({
            'title': 'Placement Ready Status',
            'message': f'Outstanding performance! Your placement readiness score is {placement_score}%. Solidify your rank by attempting live coding quizzes.',
            'category': 'Placement Readiness',
            'priority': 'low',
            'action_text': 'Attempt Live Quizzes',
            'action_url': quiz_url,
            'icon': 'bi-trophy-fill',
            'impact_badge': 'Top Placement Tier',
        })

    # 2. Big-O Complexity Master Dedicated Intelligence
    comp_lvl = user.game_complexity_level
    if comp_lvl == 0:
        recommendations.append({
            'title': 'Master Big-O Time Complexity',
            'message': 'Big-O time complexity analysis is tested in 95%+ of technical interviews. Play Big-O Complexity Master to train your speed at evaluating O(1), O(N log N), and O(N²) time limits under timer pressure.',
            'category': 'Coding Arcade',
            'priority': 'high',
            'action_text': 'Play Big-O Master',
            'action_url': f'{games_url}?game=complexity',
            'icon': 'bi-speedometer2',
            'impact_badge': 'Interview Essential',
        })
    elif comp_lvl < 5:
        recommendations.append({
            'title': f'Advance Big-O Complexity (Level {comp_lvl})',
            'message': f'You are currently at Level {comp_lvl} in Big-O Master. Advance to Level 5+ to master complex nested loop, recursion tree, and space complexity diagnostics.',
            'category': 'Coding Arcade',
            'priority': 'medium',
            'action_text': 'Continue Big-O Challenge',
            'action_url': f'{games_url}?game=complexity',
            'icon': 'bi-speedometer2',
            'impact_badge': f'Level {comp_lvl}',
        })
    else:
        recommendations.append({
            'title': f'Big-O Master Specialist (Level {comp_lvl})',
            'message': f'Excellent algorithm intuition! You have reached Level {comp_lvl} in Big-O Complexity. Maintain your edge with timed speed runs.',
            'category': 'Coding Arcade',
            'priority': 'low',
            'action_text': 'Play Speed Challenge',
            'action_url': f'{games_url}?game=complexity',
            'icon': 'bi-shield-check',
            'impact_badge': f'Level {comp_lvl} Expert',
        })

    # 3. Bug Hunter & Debugging Speed
    bug_lvl = user.game_bug_level
    if bug_lvl < 3:
        recommendations.append({
            'title': 'Improve Debugging Speed (Bug Hunter)',
            'message': f'Spot compiler errors and memory leaks faster in Bug Hunter to minimize runtime penalties during placement coding tests (Current: Level {bug_lvl}).',
            'category': 'Coding Arcade',
            'priority': 'medium',
            'action_text': 'Play Bug Hunter',
            'action_url': f'{games_url}?game=bug',
            'icon': 'bi-bug-fill',
            'impact_badge': f'Level {bug_lvl}',
        })

    # 4. DSA Category Gap & Weakness Analysis
    category_stats = []
    for category_name, problems in DSA_SHEET.items():
        cat_total = len(problems)
        cat_completed = sum(1 for p in problems if p['slug'] in completed_dsa)
        pct = (cat_completed / cat_total * 100) if cat_total > 0 else 0
        category_stats.append({
            'name': category_name,
            'total': cat_total,
            'completed': cat_completed,
            'percentage': pct,
            'slug': category_name.lower().replace(' ', '-').replace('&', 'and').replace('/', '-')
        })

    unsolved_categories = [c for c in category_stats if c['percentage'] < 100]
    if unsolved_categories:
        unsolved_categories.sort(key=lambda x: (x['percentage'], -x['total']))
        weakest = unsolved_categories[0]
        if weakest['percentage'] == 0:
            recommendations.append({
                'title': f'Target Skill Gap: {weakest["name"]}',
                'message': f'You have not solved any problems in {weakest["name"]} yet ({weakest["total"]} core interview questions available). Tackle this topic next to balance your DSA mastery.',
                'category': 'DSA & Problem Solving',
                'priority': 'high',
                'action_text': f'Practice {weakest["name"]}',
                'action_url': f'{study_url}#cat-{weakest["slug"]}',
                'icon': 'bi-code-square',
                'impact_badge': f'0/{weakest["total"]} Solved',
            })
        else:
            recommendations.append({
                'title': f'Boost {weakest["name"]} Coverage',
                'message': f'You have completed {weakest["completed"]}/{weakest["total"]} ({int(weakest["percentage"])}%) of {weakest["name"]} problems. Solve remaining questions to complete this module.',
                'category': 'DSA & Problem Solving',
                'priority': 'medium',
                'action_text': f'Continue {weakest["name"]}',
                'action_url': f'{study_url}#cat-{weakest["slug"]}',
                'icon': 'bi-graph-up-arrow',
                'impact_badge': f'{int(weakest["percentage"])}% Complete',
            })

    # 5. LeetCode Performance Diagnostics
    if not user.leetcode_username:
        recommendations.append({
            'title': 'Link LeetCode Account',
            'message': 'Link your LeetCode profile in Leaderboard to automatically synchronize solved problems and gain competitive campus ranking.',
            'category': 'LeetCode Sync',
            'priority': 'high',
            'action_text': 'Link Profile Now',
            'action_url': leaderboard_url,
            'icon': 'bi-code-slash',
            'impact_badge': 'Auto Sync Rank',
        })
    else:
        if user.leetcode_medium_solved == 0 and user.leetcode_hard_solved == 0:
            recommendations.append({
                'title': 'Tackle Medium & Hard Problems',
                'message': f'You have solved {user.leetcode_easy_solved} Easy problems on LeetCode. Technical interviews heavily emphasize Medium difficulty questions.',
                'category': 'LeetCode Strategy',
                'priority': 'high',
                'action_text': 'Solve Medium Problems',
                'action_url': study_url,
                'icon': 'bi-fire',
                'impact_badge': 'Interview Essential',
            })

    # 6. Live Quizzes Assessment
    now = timezone.now()
    live_quizzes = Quiz.objects.filter(is_live=True, start_time__lte=now, end_time__gte=now)
    user_submitted_quiz_ids = QuizSubmission.objects.filter(user=user).values_list('quiz_id', flat=True)
    unattempted_live_quizzes = live_quizzes.exclude(id__in=user_submitted_quiz_ids)

    if unattempted_live_quizzes.exists():
        target_quiz = unattempted_live_quizzes.first()
        recommendations.append({
            'title': f'Live Quiz Open: {target_quiz.title}',
            'message': f'A live coding quiz "{target_quiz.title}" is active right now! Test your speed and earn up to {target_quiz.total_xp} XP.',
            'category': 'Live Quizzes',
            'priority': 'high',
            'action_text': 'Take Live Quiz',
            'action_url': quiz_url,
            'icon': 'bi-patch-question-fill',
            'impact_badge': f'+{target_quiz.total_xp} XP Available',
        })

    # 7. Resume Analyzer & ATS Score
    try:
        latest_resume = ResumeAnalysis.objects.filter(user=user).order_by('-created_at').first()
        if not latest_resume:
            recommendations.append({
                'title': 'Analyze Resume for ATS Readiness',
                'message': 'Upload your PDF resume to receive instant AI scoring, section breakdown, and key industry skill gap analysis.',
                'category': 'Resume Analysis',
                'priority': 'medium',
                'action_text': 'Upload Resume PDF',
                'action_url': resume_url,
                'icon': 'bi-file-earmark-person-fill',
                'impact_badge': 'ATS Optimization',
            })
        else:
            if latest_resume.score < 70:
                missing_str = f" Missing sections: {', '.join(latest_resume.missing_sections[:2])}." if latest_resume.missing_sections else ""
                recommendations.append({
                    'title': f'Optimize Resume (Score: {latest_resume.score}/100)',
                    'message': f'Your resume scored {latest_resume.score}/100.{missing_str} Review detailed suggestions to make your resume stand out to top recruiters.',
                    'category': 'Resume Analysis',
                    'priority': 'high',
                    'action_text': 'Review Feedback',
                    'action_url': resume_url,
                    'icon': 'bi-file-earmark-text-fill',
                    'impact_badge': f'Score: {latest_resume.score}/100',
                })
    except Exception:
        pass

    # 8. Streak & Learning Consistency
    if user.current_streak == 0:
        recommendations.append({
            'title': 'Start Daily Activity Streak',
            'message': 'Solve 1 DSA question or complete a coding game level today to start your daily streak and earn consistency bonuses.',
            'category': 'Daily Habit',
            'priority': 'medium',
            'action_text': 'Start Streak',
            'action_url': study_url,
            'icon': 'bi-lightning-charge-fill',
            'impact_badge': 'Streak Bonus',
        })
    elif user.current_streak >= 5:
        recommendations.append({
            'title': f'Fire Streak: {user.current_streak} Days Active!',
            'message': f'Great consistency! You are on a {user.current_streak}-day learning streak. Keep up the daily practice to maintain your rank.',
            'category': 'Daily Habit',
            'priority': 'low',
            'action_text': 'Maintain Streak',
            'action_url': home_url,
            'icon': 'bi-fire',
            'impact_badge': f'{user.current_streak} Days Streak',
        })

    # Save generated recommendations cleanly
    Recommendation.objects.filter(user=user).delete()
    saved_objects = []
    for rec in recommendations:
        obj = Recommendation.objects.create(user=user, **rec)
        saved_objects.append(obj)

    return saved_objects
