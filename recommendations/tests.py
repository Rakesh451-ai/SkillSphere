from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from studylogs.models import StudyLog
from skills.models import Skill
from goals.models import Goal
from resumeanalyzer.models import ResumeAnalysis
from recommendations.models import Recommendation
from recommendations.engine import generate_recommendations

User = get_user_model()


class RecommendationEngineTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpassword',
            current_streak=0,
            longest_streak=0
        )

    def test_new_user_recommendations(self):
        """A new user with no logs, skills, goals, or resume should get onboarding recommendations."""
        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]
        categories = [r['category'] for r in recs]

        # Should recommend adding skills
        self.assertIn('Skills', categories)
        # Should welcome user and suggest logging first study session
        self.assertIn('Welcome to SkillSphere! Start your learning journey by logging your first study session to get personalized AI insights.', messages)
        # Should recommend analyzing resume
        self.assertIn('Resume', categories)

        # Check that recommendations are saved in the DB
        db_recs = Recommendation.objects.filter(user=self.user)
        self.assertEqual(db_recs.count(), len(recs))

    def test_productivity_and_burnout_recommendations(self):
        """Test study hours, productivity levels, and burnout warnings."""
        # Create some study logs for last week
        today = timezone.localdate()
        for i in range(5):
            StudyLog.objects.create(
                user=self.user,
                topic=f'Topic {i}',
                hours=Decimal('8.0'),  # Total 40 hours (triggers burnout warning)
                productivity=9,       # Avg productivity 9 (triggers peak productivity)
                category='WEBDEV',
                date=today - timedelta(days=i)
            )

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]

        # Check burnout warning (>35 hours)
        self.assertTrue(any('burnout' in msg for msg in messages))
        # Check peak productivity recommendation (>=8)
        self.assertTrue(any('Excellent productivity!' in msg for msg in messages))

    def test_study_consistency_drop(self):
        """Test drop in study hours compared to previous week."""
        today = timezone.localdate()
        # Older week: 20 hours
        for i in range(4):
            StudyLog.objects.create(
                user=self.user,
                topic=f'Older Topic {i}',
                hours=Decimal('5.0'),
                productivity=7,
                category='WEBDEV',
                date=today - timedelta(days=8 + i)
            )
        # Recent week: 5 hours (75% drop)
        StudyLog.objects.create(
            user=self.user,
            topic='Recent Topic',
            hours=Decimal('5.0'),
            productivity=7,
            category='WEBDEV',
            date=today - timedelta(days=2)
        )

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]

        # Should show a consistency drop warning
        self.assertTrue(any('dropped by 75%' in msg for msg in messages))

    def test_resume_analysis_feedback(self):
        """Test recommendations generated from resume analysis."""
        # Create a resume analysis with low score and missing sections
        ResumeAnalysis.objects.create(
            user=self.user,
            score=45,
            suggestions=['Add education info'],
            skills_found=['Python'],
            sections_found=['Skills'],
            missing_sections=['Projects', 'Certifications']
        )

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]

        # Should warn about low resume score
        self.assertTrue(any('score is low (45/100)' in msg for msg in messages))
        # Should suggest adding missing sections
        self.assertTrue(any('missing important sections: Projects, Certifications' in msg for msg in messages))

    def test_streak_encouragement(self):
        """Test that streak milestones generate recommendations."""
        self.user.current_streak = 5
        self.user.longest_streak = 5
        self.user.save()

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]

        self.assertTrue(any('5-day study streak' in msg for msg in messages))

        # Test rebuilding broken streak
        self.user.current_streak = 0
        self.user.longest_streak = 10
        self.user.save()

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]
        self.assertTrue(any('longest study streak was 10 days' in msg or 'record is a 10-day streak' in msg for msg in messages))

    def test_goals_deadline_and_completion(self):
        """Test upcoming goal deadlines and high goal completion rates."""
        today = timezone.localdate()

        # Create upcoming goal
        Goal.objects.create(
            user=self.user,
            title='Learn Django REST',
            goal_type='weekly',
            status='in_progress',
            deadline=today + timedelta(days=1)
        )

        # Create multiple completed goals to trigger high completion rate
        for i in range(3):
            Goal.objects.create(
                user=self.user,
                title=f'Goal {i}',
                status='completed',
                deadline=today - timedelta(days=2)
            )

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]

        # Check deadline warning
        self.assertTrue(any('due on' in msg and 'Django REST' in msg for msg in messages))
        # Check high goal completion rate encouragement (75% completion rate of 4 goals total)
        self.assertTrue(any('completed 75% of your goals' in msg for msg in messages))

    def test_skill_progression_suggestions(self):
        """Test suggestions based on skill category and level."""
        # Beginner WebDev
        Skill.objects.create(
            user=self.user,
            skill_name='React',
            category='WEBDEV',
            level='beginner',
            hours_practiced=5
        )
        # Close to advanced
        Skill.objects.create(
            user=self.user,
            skill_name='Python Django',
            category='DSA',  # Using DSA or WEBDEV
            level='intermediate',
            hours_practiced=85
        )

        recs = generate_recommendations(self.user)
        messages = [r['message'] for r in recs]

        # Should suggest project for Web Dev beginner
        self.assertTrue(any('beginner in Web Development' in msg for msg in messages))
        # Should suggest practicing to reach advanced
        self.assertTrue(any('close to advanced level in Python Django' in msg for msg in messages))
