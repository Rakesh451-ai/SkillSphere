import json
import urllib.request
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone

def fetch_leetcode_data(username):
    """
    Fetch LeetCode solved questions count (Easy, Medium, Hard) and recent submissions
    for a given username using the public GraphQL API.
    """
    url = "https://leetcode.com/graphql/"
    query = """
    query userProblemsSolved($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
      recentSubmissionList(username: $username, limit: 15) {
        timestamp
        statusDisplay
        titleSlug
      }
    }
    """
    
    variables = {"username": username}
    payload = {
        "query": query,
        "variables": variables
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode('utf-8')
            res_json = json.loads(res_data)
            
            if 'errors' in res_json:
                return None
                
            data_dict = res_json.get('data', {})
            matched_user = data_dict.get('matchedUser', None)
            
            if not matched_user:
                return None
                
            submission_num = matched_user.get('submitStats', {}).get('acSubmissionNum', [])
            easy_solved = 0
            medium_solved = 0
            hard_solved = 0
            
            for item in submission_num:
                diff = item.get('difficulty')
                count = item.get('count', 0)
                if diff == 'Easy':
                    easy_solved = count
                elif diff == 'Medium':
                    medium_solved = count
                elif diff == 'Hard':
                    hard_solved = count
                    
            recent_submissions = data_dict.get('recentSubmissionList', [])
            
            return {
                "easy": easy_solved,
                "medium": medium_solved,
                "hard": hard_solved,
                "recent_submissions": recent_submissions
            }
    except Exception as e:
        print(f"Error fetching LeetCode data for {username}: {e}")
        return None

def sync_leetcode_stats(user):
    """
    Sync user's LeetCode stats, award XP points for new questions solved,
    and update daily streak / check for daily progress.
    """
    if not user.leetcode_username:
        return False
        
    data = fetch_leetcode_data(user.leetcode_username)
    if not data:
        return False
        
    easy_new = data['easy']
    medium_new = data['medium']
    hard_new = data['hard']
    
    # Calculate XP earned from new questions
    # Award: Easy = 2 XP, Medium = 5 XP, Hard = 10 XP
    easy_diff = max(0, easy_new - user.leetcode_easy_solved)
    medium_diff = max(0, medium_new - user.leetcode_medium_solved)
    hard_diff = max(0, hard_new - user.leetcode_hard_solved)
    
    xp_earned = (easy_diff * 2) + (medium_diff * 5) + (hard_diff * 10)
    
    if xp_earned > 0:
        user.xp_points += xp_earned
        
    # Update solved counters
    user.leetcode_easy_solved = max(user.leetcode_easy_solved, easy_new)
    user.leetcode_medium_solved = max(user.leetcode_medium_solved, medium_new)
    user.leetcode_hard_solved = max(user.leetcode_hard_solved, hard_new)
    user.leetcode_last_sync = timezone.now()
    
    # Track daily progress according to recent submissions
    today_date = timezone.localdate()
    yesterday_date = today_date - timezone.timedelta(days=1)
    
    # Ensure completed_dsa_problems list exists
    completed_problems = user.completed_dsa_problems
    if not isinstance(completed_problems, list):
        completed_problems = []
        
    # Check if they solved an accepted question today
    solved_today = False
    for sub in data['recent_submissions']:
        if sub.get('statusDisplay') == 'Accepted':
            slug = sub.get('titleSlug')
            if slug and slug not in completed_problems:
                completed_problems.append(slug)
                
            try:
                sub_timestamp = int(sub.get('timestamp'))
                sub_date = timezone.datetime.fromtimestamp(sub_timestamp, tz=timezone.get_current_timezone()).date()
                if sub_date == today_date:
                    solved_today = True
            except Exception:
                continue
                
    user.completed_dsa_problems = completed_problems
                
    if solved_today:
        # User solved a question today!
        if user.last_activity_date == yesterday_date:
            user.current_streak += 1
        elif user.last_activity_date != today_date:
            user.current_streak = 1
        user.last_activity_date = today_date
        
        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak
    else:
        # Not solved today. Check if streak has broken
        if user.last_activity_date and user.last_activity_date < yesterday_date:
            user.current_streak = 0
            
        # Subtract points if they did not solve today and haven't been penalized today
        if user.leetcode_last_penalty_date != today_date:
            # Deduct 5 XP points, ensuring XP doesn't drop below 0
            user.xp_points = max(0, user.xp_points - 5)
            user.leetcode_last_penalty_date = today_date
            
    user.save()
    return True
