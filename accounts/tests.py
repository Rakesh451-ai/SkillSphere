from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.leetcode import sync_leetcode_stats

User = get_user_model()


class LeetCodeSyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='password123',
            leetcode_username='test_lc_user',
            xp_points=100,
            current_streak=2,
            longest_streak=2,
            last_activity_date=timezone.localdate() - timezone.timedelta(days=1)
        )

    @patch('accounts.leetcode.fetch_leetcode_data')
    def test_sync_new_solved_questions(self, mock_fetch):
        """Test awarding XP and maintaining streak when new questions are solved on LeetCode."""
        # Setup mock return value
        mock_fetch.return_value = {
            'easy': 10,
            'medium': 5,
            'hard': 1,
            'recent_submissions': [
                # Solved today
                {
                    'timestamp': str(int(timezone.now().timestamp())),
                    'statusDisplay': 'Accepted'
                }
            ]
        }

        # Sync
        success = sync_leetcode_stats(self.user)
        self.assertTrue(success)
        self.user.refresh_from_db()
        
        # Initial solved counts were 0, so new solved counts are 10 Easy, 5 Med, 1 Hard.
        # XP expected: 100 + (10*2 + 5*5 + 1*10) = 155 XP.
        self.assertEqual(self.user.leetcode_easy_solved, 10)
        self.assertEqual(self.user.leetcode_medium_solved, 5)
        self.assertEqual(self.user.leetcode_hard_solved, 1)
        self.assertEqual(self.user.xp_points, 155)
        
        # Streak should be incremented since last_activity_date was yesterday and solved today
        self.assertEqual(self.user.current_streak, 3)
        self.assertEqual(self.user.last_activity_date, timezone.localdate())

    @patch('accounts.leetcode.fetch_leetcode_data')
    def test_sync_no_activity_penalty(self, mock_fetch):
        """Test streak breaking and XP penalty if no questions are solved today."""
        # Setup mock return value - no recent submissions or no accepted ones
        mock_fetch.return_value = {
            'easy': 5,
            'medium': 2,
            'hard': 0,
            'recent_submissions': [
                {
                    # Older submission (3 days ago)
                    'timestamp': str(int((timezone.now() - timezone.timedelta(days=3)).timestamp())),
                    'statusDisplay': 'Accepted'
                }
            ]
        }
        
        # Set user's initial solved count to match mock to isolate streak penalty
        self.user.leetcode_easy_solved = 5
        self.user.leetcode_medium_solved = 2
        self.user.leetcode_hard_solved = 0
        # Set last activity date to 3 days ago to check streak breaking
        self.user.last_activity_date = timezone.localdate() - timezone.timedelta(days=3)
        self.user.save()

        success = sync_leetcode_stats(self.user)
        self.assertTrue(success)
        self.user.refresh_from_db()

        # Streak should be broken (set to 0) because they didn't solve today and last was 3 days ago
        self.assertEqual(self.user.current_streak, 0)
        # XP should be penalized by 5 (100 - 5 = 95)
        self.assertEqual(self.user.xp_points, 95)
        self.assertEqual(self.user.leetcode_last_penalty_date, timezone.localdate())
        
        # Verify penalty is only applied once per day: syncing again shouldn't subtract more
        success = sync_leetcode_stats(self.user)
        self.assertTrue(success)
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp_points, 95)


class ProfileAccessTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123',
            first_name='User',
            last_name='Two'
        )

    def test_view_own_profile(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Edit Profile Details')

    def test_view_other_profile(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get('/accounts/profile/?username=user2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Profile')
        self.assertContains(response, 'Viewing Profile: User Two')
        self.assertContains(response, 'Read-only Profile')
        # Ensure edit form header is NOT present
        self.assertNotContains(response, 'Edit Profile Details')

    def test_post_other_profile_fails(self):
        self.client.login(username='user1', password='password123')
        # Try to post data targeting user2's profile
        response = self.client.post('/accounts/profile/?username=user2', {
            'first_name': 'Hacked Name',
        })
        # Should redirect back to user2's profile view
        self.assertRedirects(response, '/accounts/profile/?username=user2')
        self.user2.refresh_from_db()
        # Verify first_name was NOT updated
        self.assertEqual(self.user2.first_name, 'User')


