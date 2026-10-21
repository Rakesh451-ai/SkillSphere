from django.test import TestCase
from django.contrib.auth import get_user_model

from resume_analysis.models import ResumeAnalysis
from recommendations.models import Recommendation
from recommendations.engine import generate_recommendations

User = get_user_model()


class RecommendationEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpassword',
            current_streak=0,
            longest_streak=0
        )

    def test_new_user_recommendations(self):
        recs = generate_recommendations(self.user)
        categories = [r.category for r in recs]

        # Should recommend connecting LeetCode, uploading resume, and placement readiness
        self.assertIn('Resume Analysis', categories)
        self.assertIn('Placement Readiness', categories)
        self.assertIn('Coding Arcade', categories)

        db_recs = Recommendation.objects.filter(user=self.user)
        self.assertEqual(db_recs.count(), len(recs))

    def test_big_o_master_recommendation(self):
        # Level 0
        recs = generate_recommendations(self.user)
        big_o_rec = next((r for r in recs if 'Big-O' in r.title), None)
        self.assertIsNotNone(big_o_rec)
        self.assertIn('?game=complexity', big_o_rec.action_url)

        # Level 3
        self.user.game_complexity_level = 3
        self.user.save()
        recs = generate_recommendations(self.user)
        big_o_rec = next((r for r in recs if 'Big-O' in r.title), None)
        self.assertIsNotNone(big_o_rec)
        self.assertIn('Level 3', big_o_rec.title)

    def test_resume_analysis_feedback(self):
        ResumeAnalysis.objects.create(
            user=self.user,
            score=45,
            suggestions=['Add education info'],
            skills_found=['Python'],
            sections_found=['Skills'],
            missing_sections=['Projects', 'Certifications']
        )

        recs = generate_recommendations(self.user)
        messages = [r.message for r in recs]

        self.assertTrue(any('45/100' in msg for msg in messages))

    def test_streak_encouragement(self):
        self.user.current_streak = 5
        self.user.save()

        recs = generate_recommendations(self.user)
        self.assertTrue(any('5 Days Active' in r.title or '5-day' in r.message for r in recs))
