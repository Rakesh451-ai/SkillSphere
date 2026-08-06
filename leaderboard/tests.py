from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class LeaderboardStreakTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123',
            current_streak=5,
            leetcode_username='leetcode1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123',
            current_streak=12,
            leetcode_username='leetcode2'
        )

    def test_leaderboard_sorted_by_streak(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('leaderboard:leaderboard') + '?sort=streak')
        self.assertEqual(response.status_code, 200)
        ranked_users = response.context['ranked_users']
        self.assertEqual(len(ranked_users), 2)
        # user2 has 12 streak, so user2 should be rank 1
        self.assertEqual(ranked_users[0]['user'], self.user2)
        self.assertEqual(ranked_users[1]['user'], self.user1)

